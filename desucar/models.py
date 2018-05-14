from django.db import models
from django.contrib.humanize.templatetags.humanize import intcomma


class Maker(models.Model):
    name = models.CharField(max_length=30)
    contact = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return '{name}'.format(name=self.name)


class Car(models.Model):
    maker = models.ForeignKey(Maker, on_delete=models.CASCADE, related_name='cars')
    name = models.CharField(max_length=30)  # 5세대(HG) 그랜저, 3세대(JA) 올 뉴 모닝
    simple_name = models.CharField(max_length=20)  # 그랜저, 모닝
    search_keywords = models.TextField(null=True, blank=True)
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
    car_detail = models.TextField()
    kind = models.CharField(max_length=2, choices=(
        (종류.리콜, '리콜'),
        (종류.무상수리, '무상수리'),
    ))
    n_targets = models.IntegerField(null=True, blank=True)
    n_targets_comment = models.CharField(max_length=30, null=True, blank=True)
    part_name = models.CharField(max_length=20)
    solution = models.TextField()
    source_name = models.CharField(max_length=50)
    source_url = models.URLField(null=True, blank=True)
    make_start = models.DateField(null=True)
    make_end = models.DateField(null=True)
    make_date_comment = models.CharField(max_length=30, null=True, blank=True)
    fix_start = models.CharField(max_length=40, null=True, blank=True)
    fix_end = models.CharField(max_length=40, null=True, blank=True)
    
    @property
    def n_targets_str(self):
        if not self.n_targets and not self.n_targets_comment:
            return ''
        elif self.n_targets_comment:
            return self.n_targets_comment
        else:
            return intcomma(self.n_targets) + ' 대'

    def __str__(self):
        return '{name} - {part}'.format(name=self.car.name, part=self.part_name)


class Community(models.Model):
    name = models.CharField(max_length=40)
    url = models.URLField()
    n_members = models.IntegerField(null=True)
    is_active = models.BooleanField()


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
    author_name = models.CharField(max_length=30)
    join_required = models.BooleanField()


class SuddenAccelReport(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='sudden_accels')
    car_detail = models.CharField(max_length=40, null=True)
    buy_at = models.DateField(null=True, blank=True)
    make_at = models.DateField(null=True, blank=True)
    accident_at = models.DateField(null=True, blank=True)

    detail = models.TextField()
    source = models.CharField(max_length=200)
