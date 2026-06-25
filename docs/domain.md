# Domain and user workflows

## Roles

A user record can contain student, teacher, and administrator flags. The
displayed `UserDTO.role` resolves them in this priority:

1. administrator;
2. teacher;
3. student;
4. not defined.

New `/start` registrations are students. An administrator grants teacher
status with `/make_teacher <username>`.

## Domain entities

### User

Stores the Telegram username, name, chat ID, role flags, UUID, and audit
timestamps. Username and UUID are unique.

### Lesson

A teacher-owned subject or lesson type with a label, duration in minutes, and
price. A lesson can be assigned to a teacher/student relationship.

### TeacherStudent

Links one teacher and one student. The pair is unique. The optional lesson UUID
records the lesson currently assigned to that relationship.

### Slot

A teacher-owned date/time that may be booked by a student. A teacher cannot
have two slots with the same start timestamp. Booking fills `uuid_student` and
`dt_spot`.

## Entity relationships

```text
User (teacher) 1 ─── * Lesson
User (teacher) 1 ─── * Slot * ─── 0..1 User (student)
User (teacher) 1 ─── * TeacherStudent * ─── 1 User (student)
Lesson         1 ─── * TeacherStudent
```

## Commands

| Command | Purpose |
| --- | --- |
| `/start` | Register the Telegram user as a student and send a greeting |
| `/menu` | Show the main menu for the injected user role |
| `/cancel` | Clear current FSM state and return to the role menu |
| `/make_teacher <username>` | Admin-only promotion of a registered user |
| `/produce` | Development command that publishes a test message to a hard-coded chat ID |

`/produce` is diagnostic code and should not be treated as a production user
feature.

## Teacher workflows

### Manage students

From `Menu → Students`, a teacher can:

- list attached students;
- enter one or more Telegram usernames to attach students;
- inspect a student and their assigned lessons;
- attach or detach a lesson;
- remove the teacher/student relationship.

Removing a student from a teacher also deletes slots booked by that student.

### Manage lessons

From `Menu → Lessons`, a teacher can:

- list lessons;
- create a lesson through label, duration, and price FSM steps;
- inspect a lesson;
- update one field or the whole lesson;
- detach the lesson from students and then delete it.

### Manage slots

From `Menu → Slots`, a teacher selects the current or next week and sends a
plain-text schedule. The parser recognizes weekday aliases from Monday through
Friday and `HH:MM` values.

Example:

```text
понедельник 10:00 11:30
среда 15:00
пт 09:00 12:00
```

The bot previews parsed slots. On confirmation:

- create mode inserts all slots;
- update mode compares timestamps for the selected ISO week, deletes removed
  slots, and inserts new ones.

After saving, the teacher can send free slots to eligible students. Each
student receives buttons grouped by day, then by time.

The schedule formatter can also calculate daily and weekly lesson counts and
income from booked slots and assigned lesson prices.

## Student booking workflow

1. A teacher sends available slots.
2. The student selects a day.
3. The bot reloads free slots for that teacher and day.
4. The student selects a time.
5. The slot is assigned to the student and the booking timestamp is stored.
6. The student receives a confirmation and an option to book another slot.
7. The teacher receives a booking notification.

The current repository update does not use a conditional
`WHERE uuid_student IS NULL`, so simultaneous clicks are not protected by an
atomic booking guard. See [Operations](operations.md#known-operational-caveats).

## Current UI scope

Teacher flows are the most complete. Student submenu entries for browsing
teachers and lessons are currently placeholders. Administration is primarily
command-driven; there is no full admin inline-menu workflow.

