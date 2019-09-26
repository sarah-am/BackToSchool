import django_tables2 as tables
from .models import Semester, Classroom, Student, Attendance

class StudentTable(tables.Table):
    class Meta:
        model = Student


class TableView(tables.SingleTableView):
    table_class = StudentTable
    queryset = Student.objects.all()
    template_name = "student_list2.html"