from datetime import datetime, timedelta, time
from django.core.management.base import BaseCommand
from doctors.models import Doctors, TimeSlot
from django.utils.timezone import make_aware

class Command(BaseCommand):
    help = 'Generates time slots for doctors based on their availability'

    def handle(self, *args, **kwargs):
        # Your generate_timeslots logic here
        today = datetime.today().date()
        end_date = today + timedelta(days=14)

        working_hours_start = time(9, 0)
        working_hours_end = time(17, 0)
        break_start = time(12, 0)
        break_end = time(14, 0)
        slot_duration = timedelta(minutes=30)

        weekday_map = {
            'Monday': 0,
            'Tuesday': 1,
            'Wednesday': 2,
            'Thursday': 3,
            'Friday': 4,
            'Saturday': 5,
            'Sunday': 6
        }

        for doctor in Doctors.objects.all():
            doctor_days = [weekday_map[day] for day in doctor.availability]

            current_date = today
            while current_date <= end_date:
                if current_date.weekday() in doctor_days:
                    current_time = datetime.combine(current_date, working_hours_start)
                    day_end = datetime.combine(current_date, working_hours_end)

                    while current_time + slot_duration <= day_end:
                        slot_end = current_time + slot_duration

                        # Skip break hours
                        if not (break_start <= current_time.time() < break_end):
                            exists = TimeSlot.objects.filter(
                                doctor=doctor,
                                appointment_date=current_date,
                                start_time=current_time.time(),
                                end_time=slot_end.time()
                            ).exists()

                            if not exists:
                                TimeSlot.objects.create(
                                    doctor=doctor,
                                    appointment_date=current_date,
                                    start_time=current_time.time(),
                                    end_time=slot_end.time()
                                )
                        current_time = slot_end
                current_date += timedelta(days=1)

        self.stdout.write(self.style.SUCCESS('Successfully generated time slots for doctors.'))
