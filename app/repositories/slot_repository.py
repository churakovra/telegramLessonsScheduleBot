from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select, func, and_, update
from sqlalchemy.orm import Session

from app.db.orm.slot import Slot
from app.schemas.slot_dto import SlotDTO


class SlotRepository:
    def __init__(self, session: Session):
        self._db = session

    def add_slot(self, slot_dto: SlotDTO):
        slot = Slot.new_instance(slot_dto)
        self._db.add(slot)
        self._db.commit()
        self._db.refresh(slot)

    def get_slot(self, slot_uuid: UUID):
        stmt = select(Slot).where(Slot.uuid == slot_uuid)
        slot = self._db.scalar(stmt)
        return slot

    def get_free_slots(self, teacher_uuid: UUID) -> list[SlotDTO]:
        slots = list()
        stmt = (
            select(Slot)
            .where(
                and_(
                    Slot.teacher == teacher_uuid,
                    Slot.dt_add > func.now(),
                    Slot.uuid_student == None
                )
            )
        )
        for slot in self._db.scalars(stmt):
            slots.append(SlotDTO.to_dto(slot))
        return slots

    def assign_slot(self, student_uuid: UUID, slot_uuid: UUID):
        stmt = (
            update(Slot)
            .where(Slot.uuid == slot_uuid)
            .values(uuid_student=student_uuid)
            .values(dt_spot=datetime.now(timezone.utc).astimezone())
        )
        self._db.execute(stmt)
        self._db.commit()
