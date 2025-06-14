from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from scheduler.models import DateTimeSlot
from scheduler.organization.models import Organization
from scheduler.room.models import Room
from scheduler.faculty.models import Faculty
from scheduler.course.models import Course
from scheduler.group.models import Group


class TimeTable(models.Model):
    organization = models.ForeignKey(to=Organization, on_delete=models.CASCADE)
    timetable_id = models.CharField(max_length=50)
    year = models.PositiveSmallIntegerField(validators=(
        MinValueValidator(limit_value=1900, message='Year cannot be less than 1900'),
        MaxValueValidator(limit_value=2100, message='Year cannot be more than 2100'),
    ))
    semester = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.organization.name} - {self.year} - {self.semester}"

    class Meta:
        unique_together = ('organization', 'timetable_id')

    # Method to generate a unique timetable_id
    def save(self, *args, **kwargs):
        if not self.timetable_id:
            last_id = TimeTable.objects.filter(
                organization=self.organization,
                year=self.year,
                semester=self.semester
            ).count()
            self.timetable_id = f"{self.year}-{self.semester}-{last_id}"
        super().save(*args, **kwargs)


class Section(models.Model):
    timetable = models.ForeignKey(to=TimeTable, on_delete=models.CASCADE)
    faculty = models.ForeignKey(to=Faculty, null=True, on_delete=models.SET_NULL)
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    group = models.ForeignKey(to=Group, on_delete=models.CASCADE)
    duration = models.PositiveSmallIntegerField(blank=True, default=1)

    def __str__(self):
        return f"{self.course} - {self.group} - {self.faculty}"

class Slot(models.Model):
    section = models.OneToOneField(to=Section, on_delete=models.CASCADE)
    room = models.ForeignKey(to=Room, null=True, on_delete=models.SET_NULL)
    date_time_slot = models.ForeignKey(to=DateTimeSlot, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.date_time_slot} - {self.room} - {self.section}"


class ScheduleStatus(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('RUNNING', 'Running'),
        ('SUCCESS', 'Success'),
        ('FAILURE', 'Failure'),
    ]

    timetable = models.OneToOneField(TimeTable, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    task_id = models.CharField(max_length=100, null=True, blank=True)
    last_run_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.timetable.timetable_id} - {self.status}"