from django.db import models


class Maker(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return '{name}'.format(name=self.name)


class Car(models.Model):
    maker = models.ForeignKey(Maker, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)  # 5세대(HG) 그랜저, 3세대(JA) 올 뉴 모닝
    simple_name = models.CharField(max_length=20)  # 그랜저, 모닝
    code = models.CharField(max_length=10)
    make_start = models.DateField()
    make_end = models.DateField(null=True, blank=True)

    @property
    def year(self):
        return self.make_start.year

    def __str__(self):
        return '{name}'.format(name=self.name)


class OfficialDefect(models.Model):
    class 종류:
        리콜 = 'RC'
        무상수리 = 'FF'
        
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='official_defects')
    kind = models.CharField(max_length=2, choices=(
        (종류.리콜, '리콜'),
        (종류.무상수리, '무상수리'),
    ))
    n_targets = models.IntegerField(null=True, blank=True)
    part_name = models.CharField(max_length=20)
    solution = models.TextField()
    source = models.URLField(null=True, blank=True)
    make_start = models.DateField(null=True)
    make_end = models.DateField(null=True)
    fix_start = models.CharField(max_length=40, null=True, blank=True)
    fix_end = models.CharField(max_length=40, null=True, blank=True)

    def __str__(self):
        return '{name} - {part}'.format(name=self.car.name, part=self.part_name)


class Community(models.Model):
    name = models.CharField(max_length=40)
    url = models.URLField()


class CommunityDefect(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='community_defects')
    community = models.ForeignKey(Community, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=20)
    part_name = models.CharField(max_length=30, null=True, blank=True)


class CommunityDefectPost(models.Model):
    defect = models.ForeignKey(CommunityDefect, on_delete=models.CASCADE, related_name='posts')
    url = models.URLField()
    content = models.TextField(null=True, blank=True)
    posted_at = models.DateField(null=True, blank=True)
    join_required = models.BooleanField()


class SuddenAccelReport(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='sudden_accels')
    car_detail = models.CharField(max_length=40, null=True)
    buy_at = models.DateField(null=True, blank=True)
    make_at = models.DateField(null=True, blank=True)
    accident_at = models.DateField(null=True, blank=True)

    detail = models.TextField()
    source = models.CharField(max_length=200)
