from django.db import models


class Maker(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return '{name}'.format(name=self.name)


class Car(models.Model):
    maker = models.ForeignKey(Maker, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)  # 싼타페, 소나타

    def __str__(self):
        return '{name}'.format(name=self.name)


class Revision(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    production_start = models.DateField()
    production_end = models.DateField(null=True, blank=True)

    def __str__(self):
        return '{name}'.format(name=self.car.name)

# class Manufactured(models.Model):
#     start_year =
#     start_month =
#     end_year =
#     end_month =


class Defect(models.Model):
    target = models.ForeignKey(Revision, on_delete=models.CASCADE)
    n_targets = models.IntegerField()  # 대상 차량 수
    part_name = models.CharField(max_length=20)
    solution = models.TextField()
    source = models.URLField()

    def __str__(self):
        return '{name} - {part}'.format(name=self.target.car.name, part=self.part_name)
