# Generated by Django 2.1.4 on 2020-05-23 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='achieve_keyword_tab',
            fields=[
                ('AchieveKeyId', models.AutoField(primary_key=True, serialize=False)),
                ('KeyId', models.IntegerField()),
                ('a_id', models.IntegerField()),
            ],
            options={
                'db_table': 'achieve_keyword_tab',
            },
        ),
        migrations.CreateModel(
            name='achievement_authen_tab',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('scholar_id', models.IntegerField()),
                ('all_id', models.CharField(max_length=150)),
                ('a_name', models.CharField(max_length=150)),
                ('year', models.CharField(max_length=5)),
                ('author_name', models.CharField(max_length=150)),
                ('citation', models.IntegerField()),
                ('j_a_name', models.CharField(max_length=150)),
                ('file', models.CharField(max_length=150)),
                ('link', models.CharField(max_length=150)),
                ('kind', models.CharField(max_length=10)),
                ('num_view', models.IntegerField(default=0)),
                ('keyword', models.CharField(default='NULL', max_length=200)),
                ('brief', models.CharField(default='NULL', max_length=600)),
            ],
            options={
                'db_table': 'achievement_authen_tab',
            },
        ),
        migrations.CreateModel(
            name='achievement_brief_tab',
            fields=[
                ('achbfId', models.AutoField(primary_key=True, serialize=False)),
                ('a_id', models.IntegerField()),
                ('brief', models.CharField(max_length=100)),
                ('number', models.IntegerField()),
                ('next_id', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'achievement_brief_tab',
            },
        ),
        migrations.CreateModel(
            name='achievement_tab',
            fields=[
                ('a_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('year', models.CharField(max_length=5)),
                ('author_name', models.CharField(max_length=150)),
                ('citation', models.IntegerField(default=-1)),
                ('j_a_name', models.CharField(max_length=150)),
                ('file', models.CharField(max_length=150)),
                ('link', models.CharField(max_length=150)),
                ('kind', models.CharField(max_length=10)),
                ('num_view', models.IntegerField(default=0)),
                ('get_id', models.IntegerField(default=0)),
                ('brief', models.IntegerField(default=0)),
                ('keyword', models.CharField(default='NULL', max_length=200)),
            ],
            options={
                'db_table': 'achievement_tab',
            },
        ),
        migrations.CreateModel(
            name='admin_tab',
            fields=[
                ('id', models.CharField(max_length=7, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=16)),
                ('errors', models.IntegerField()),
            ],
            options={
                'db_table': 'admin_tab',
            },
        ),
        migrations.CreateModel(
            name='authen_tab',
            fields=[
                ('authen_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=30)),
                ('name', models.CharField(max_length=30)),
                ('sno', models.CharField(max_length=30)),
                ('school', models.CharField(max_length=30)),
                ('department', models.IntegerField()),
                ('identity', models.SmallIntegerField(choices=[(0, '普通用户'), (1, '学者用户'), (2, '学生用户')])),
            ],
            options={
                'db_table': 'authen_tab',
            },
        ),
        migrations.CreateModel(
            name='collect_achievement_tab',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField()),
                ('a_id', models.IntegerField()),
            ],
            options={
                'db_table': 'collect_achievement_tab',
            },
        ),
        migrations.CreateModel(
            name='collect_scholar_tab',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField()),
                ('scholar_id', models.IntegerField()),
            ],
            options={
                'db_table': 'collect_scholar_tab',
            },
        ),
        migrations.CreateModel(
            name='department_tab',
            fields=[
                ('d_id', models.AutoField(primary_key=True, serialize=False)),
                ('number', models.CharField(max_length=2)),
                ('name', models.CharField(max_length=30)),
                ('brief', models.CharField(max_length=600)),
            ],
            options={
                'db_table': 'department_tab',
            },
        ),
        migrations.CreateModel(
            name='information_tab',
            fields=[
                ('infoId', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('information', models.CharField(max_length=400)),
            ],
            options={
                'db_table': 'information_tab',
            },
        ),
        migrations.CreateModel(
            name='keyword_tab',
            fields=[
                ('keyId', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('brief', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'keyword_tab',
            },
        ),
        migrations.CreateModel(
            name='new_relation_tab',
            fields=[
                ('a_id', models.AutoField(primary_key=True, serialize=False)),
                ('auth_id', models.IntegerField(default=0)),
                ('ach_id', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'new_relation_tab',
            },
        ),
        migrations.CreateModel(
            name='person_inform_tab',
            fields=[
                ('personInfId', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField()),
                ('title', models.CharField(max_length=100)),
                ('information', models.CharField(max_length=400)),
            ],
            options={
                'db_table': 'person_inform_tab',
            },
        ),
        migrations.CreateModel(
            name='report_tab',
            fields=[
                ('r_id', models.AutoField(primary_key=True, serialize=False)),
                ('typeR', models.IntegerField(default=0)),
                ('id', models.IntegerField()),
                ('a_id', models.IntegerField()),
                ('user_name', models.CharField(max_length=100)),
                ('information', models.CharField(max_length=300)),
                ('flag', models.IntegerField()),
            ],
            options={
                'db_table': 'report_tab',
            },
        ),
        migrations.CreateModel(
            name='reserch_direction_tab',
            fields=[
                ('researchd_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'reserch_direction_tab',
            },
        ),
        migrations.CreateModel(
            name='sch_ach_authen_tab',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('student_id', models.IntegerField()),
                ('a_id', models.IntegerField()),
            ],
            options={
                'db_table': 'sch_ach_authen_tab',
            },
        ),
        migrations.CreateModel(
            name='scholar_achievement_tab',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('scholar_id', models.IntegerField()),
                ('a_id', models.IntegerField()),
            ],
            options={
                'db_table': 'scholar_achievement_tab',
            },
        ),
        migrations.CreateModel(
            name='scholar_brief_intro_tab',
            fields=[
                ('sbf_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField()),
                ('brief', models.CharField(max_length=100)),
                ('number', models.IntegerField()),
                ('next_id', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'scholar_brief_intro_tab',
            },
        ),
        migrations.CreateModel(
            name='scholar_change_tab',
            fields=[
                ('ScholarCid', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField()),
                ('scholar_id', models.IntegerField()),
                ('school', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=30)),
                ('p_title', models.CharField(max_length=30)),
                ('flag', models.IntegerField()),
                ('Scholar_Number', models.CharField(max_length=30)),
                ('Has_Info', models.IntegerField(default=0)),
                ('brief', models.IntegerField(default=0)),
                ('get_id', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'scholar_change_tab',
            },
        ),
        migrations.CreateModel(
            name='scholar_department_tab',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('scholar_id', models.IntegerField()),
                ('d_id', models.IntegerField()),
            ],
            options={
                'db_table': 'scholar_department_tab',
            },
        ),
        migrations.CreateModel(
            name='scholar_direction_tab',
            fields=[
                ('schReseaid', models.AutoField(primary_key=True, serialize=False)),
                ('scholar_id', models.IntegerField()),
                ('researchd_id', models.IntegerField()),
            ],
            options={
                'db_table': 'scholar_direction_tab',
            },
        ),
        migrations.CreateModel(
            name='scholar_tab',
            fields=[
                ('user_id', models.IntegerField()),
                ('scholar_id', models.AutoField(primary_key=True, serialize=False)),
                ('school', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=30)),
                ('p_title', models.CharField(max_length=30)),
                ('flag', models.IntegerField()),
                ('Scholar_Number', models.CharField(max_length=30)),
                ('Has_Info', models.IntegerField(default=0)),
                ('brief', models.IntegerField(default=0)),
                ('get_id', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'scholar_tab',
            },
        ),
        migrations.CreateModel(
            name='stuachievement_tab',
            fields=[
                ('a_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('year', models.CharField(max_length=5)),
                ('author_name', models.CharField(max_length=150)),
                ('citation', models.IntegerField(default=-1)),
                ('j_a_name', models.CharField(max_length=150)),
                ('file', models.CharField(max_length=150)),
                ('link', models.CharField(max_length=150)),
                ('kind', models.CharField(max_length=10)),
                ('num_view', models.IntegerField(default=0)),
                ('brief', models.IntegerField(default=0)),
                ('keyword', models.CharField(default='NULL', max_length=200)),
            ],
            options={
                'db_table': 'stuachievement_tab',
            },
        ),
        migrations.CreateModel(
            name='student_achievement_tab',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('student_id', models.IntegerField()),
                ('a_id', models.IntegerField()),
            ],
            options={
                'db_table': 'student_achievement_tab',
            },
        ),
        migrations.CreateModel(
            name='student_department_tab',
            fields=[
                ('sd_id', models.AutoField(primary_key=True, serialize=False)),
                ('student_id', models.IntegerField()),
                ('d_id', models.IntegerField()),
            ],
            options={
                'db_table': 'student_department_tab',
            },
        ),
        migrations.CreateModel(
            name='student_tab',
            fields=[
                ('user_id', models.IntegerField()),
                ('student_id', models.AutoField(primary_key=True, serialize=False)),
                ('school', models.CharField(max_length=30)),
                ('sno', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=30)),
            ],
            options={
                'db_table': 'student_tab',
            },
        ),
        migrations.CreateModel(
            name='user_authen_tab',
            fields=[
                ('authen_id', models.IntegerField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField()),
            ],
            options={
                'db_table': 'user_authen_tab',
            },
        ),
        migrations.CreateModel(
            name='user_tab',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=30)),
                ('wechatid', models.CharField(max_length=30)),
                ('authority', models.SmallIntegerField(choices=[(0, '普通用户'), (1, '学者用户'), (2, '学生用户')], default=0)),
            ],
            options={
                'db_table': 'user_tab',
            },
        ),
    ]
