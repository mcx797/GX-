from django.db import models
import django.utils.timezone as timezone
# Create your models here.
# class alluser(models.Model):



'''
管理员信息
'''
class admin_tab(models.Model):
    id = models.CharField(max_length=7, primary_key=True)
    password = models.CharField(max_length=16)
    errors = models.IntegerField()

    class Meta:
        # managed = False
        db_table = 'admin_tab'

'''
成果表,摘要和关键词放外表（一会写摘要和关键词）
'''
class achievement_tab(models.Model):
    a_id = models.AutoField(primary_key=True)  # 主键，标识id
    name = models.CharField(max_length=150)  # 成果名
    year = models.CharField(max_length=5)    #成果年份
    author_name = models.CharField(max_length=150) #作者名
    citation = models.IntegerField(default = -1)   # 被引数,若未爬到数据设为-1
    j_a_name = models.CharField(max_length=150)   #成果出处
    file = models.CharField(max_length=150)       #文件在服务器中的位置， 没有时为null
    link = models.CharField(max_length=150)       #文件链接（只保留一个）
    kind = models.CharField(max_length =10) #文献类型
    num_view = models.IntegerField(default=0)#浏览次数
    get_id = models.IntegerField(default=0)  #在原系统中的id,用于关联
    brief = models.IntegerField(default = 0) #记录简介的第一项在AchieveBreif里的id
    
    keyword = models.CharField(max_length=200, default="NULL")

    class Meta:
        # managed = False
        db_table = 'achievement_tab'
        
        
        
        
'''
学生成果表
'''
class stuachievement_tab(models.Model):
    a_id = models.AutoField(primary_key=True)  # 主键，标识id
    name = models.CharField(max_length=150)  # 成果名
    year = models.CharField(max_length=5)    #成果年份
    author_name = models.CharField(max_length=150) #作者名
    citation = models.IntegerField(default = -1)   # 被引数,若未爬到数据设为-1
    j_a_name = models.CharField(max_length=150)   #成果出处
    file = models.CharField(max_length=150)       #文件在服务器中的位置， 没有时为null
    link = models.CharField(max_length=150)       #文件链接（只保留一个）
    kind = models.CharField(max_length =10) #文献类型
    num_view = models.IntegerField(default=0)#浏览次数
    brief = models.IntegerField(default = 0) #记录简介的第一项在AchieveBreif里的id
    
    keyword = models.CharField(max_length=200, default="NULL")

    class Meta:
        # managed = False
        db_table = 'stuachievement_tab'
              
'''
学生与成果的关联表
'''
class student_achievement_tab(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.IntegerField()
    a_id = models.IntegerField()

    class Meta:
        # managed = False
        db_table = 'student_achievement_tab'
        



'''
成果简介表
'''       

class achievement_brief_tab(models.Model):
    achbfId = models.AutoField(primary_key=True)  #id
    a_id = models.IntegerField()   #成果id
    brief = models.CharField(max_length = 100)  #简介
    number = models.IntegerField()              #表示是简介中的第几段
    next_id = models.IntegerField(default = 0)  #下一段的achbfId.
    
    class Meta:
        # managed = False
        db_table = 'achievement_brief_tab'
 
        

'''
关键词表
'''     

class keyword_tab(models.Model):
    keyId = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 20)
    brief = models.CharField(max_length = 200)
    class Meta:
        # managed = False
        db_table = 'keyword_tab'       
        
        

'''
成果关键词关联表
'''
class achieve_keyword_tab(models.Model):
    AchieveKeyId = models.AutoField(primary_key = True)
    KeyId = models.IntegerField()
    a_id = models.IntegerField()
    class Meta:
        # managed = False
        db_table = 'achieve_keyword_tab'

  

'''
学者新提交但未经认证的成果表
一个作者提交，但可能有多个学者, 其他作者
提交的人进行查找
1. 搜索    （）
2.  part1:字符串  （）   （所有的作者的姓名信息，不管有无id）
    part2:id1,id2,id3
'''
class achievement_authen_tab(models.Model):
    id = models.AutoField(primary_key=True)
    scholar_id = models.IntegerField()  #提交的人的id
    all_id = models.CharField(max_length=150)#所有的可关联作者的id, 以，分开
    a_name = models.CharField(max_length=150)#成果名
    year = models.CharField(max_length=5)
    author_name = models.CharField(max_length=150)  #所有作者名，以，分开
    citation = models.IntegerField()
    j_a_name = models.CharField(max_length=150)
    file = models.CharField(max_length=150)
    link = models.CharField(max_length=150)
    kind = models.CharField(max_length =10) #文献类型
    num_view = models.IntegerField(default=0)#浏览次数
    keyword = models.CharField(max_length=200, default="NULL")#关键词，以，分开
    brief = models.CharField(max_length = 600, default='NULL')

    class Meta:
        # managed = False
        db_table = 'achievement_authen_tab'
        
                
'''
用于认证的表：学者在小程序端希望关联一个成果后存放此表。
'''
class sch_ach_authen_tab(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.IntegerField()
    a_id = models.IntegerField()

    class Meta:
        # managed = False
        db_table = 'sch_ach_authen_tab'        
     

'''
通过认证的学者与成果的关联表
'''
class scholar_achievement_tab(models.Model):
    id = models.AutoField(primary_key=True)
    scholar_id = models.IntegerField()
    a_id = models.IntegerField()

    class Meta:
        # managed = False
        db_table = 'scholar_achievement_tab'



'''
记录学院信息
'''
class department_tab(models.Model):
    d_id = models.AutoField(primary_key=True) #学院id
    number = models.CharField(max_length=2)   #学院号
    name = models.CharField(max_length=30)    #学院名称
    brief = models.CharField(max_length=600)  #学院简介

    class Meta:
        # managed = False
        db_table = 'department_tab'

'''
用于记录所有的学者信息
'''
class scholar_tab(models.Model):
    user_id = models.IntegerField()#学者对应的用户id, 未认领时为-1
    scholar_id = models.AutoField(primary_key=True)#学者在我们系统中的id，唯一标识
    school = models.CharField(max_length=30)#学者学校
    name = models.CharField(max_length=30)#学者姓名
    email = models.CharField(max_length=30)#学者邮箱
    p_title = models.CharField(max_length=30)#职称
    flag = models.IntegerField()              #标志位
    Scholar_Number = models.CharField(max_length = 30) #学者的工号
    Has_Info = models.IntegerField(default = 0) #判断是否有需要认领的信息
    brief = models.IntegerField(default = 0) #记录是否有简介，有则为对应的简介
                                             #的sbf_id， 没有为0
    get_id = models.IntegerField(default=0)
    class Meta:
        # managed = False
        db_table = 'scholar_tab'


'''
用于修改学者的信息
'''
class scholar_change_tab(models.Model):
    ScholarCid = models.AutoField(primary_key = True)
    user_id = models.IntegerField()#学者对应的用户id, 未认领时为-1
    scholar_id = models.IntegerField()#学者在我们系统中的id，唯一标识
    school = models.CharField(max_length=30)#学者学校
    name = models.CharField(max_length=30)#学者姓名
    email = models.CharField(max_length=30)#学者邮箱
    p_title = models.CharField(max_length=30)#职称
    flag = models.IntegerField()              #标志位
    Scholar_Number = models.CharField(max_length = 30) #学者的工号
    Has_Info = models.IntegerField(default = 0) #判断是否有需要认领的信息
    brief = models.IntegerField(default = 0) #记录是否有简介，有则为对应的简介
                                             #的sbf_id， 没有为0
    get_id = models.IntegerField(default=0)
    class Meta:
        # managed = False
        db_table = 'scholar_change_tab'


'''
公告信息
'''

class information_tab(models.Model):
    infoId = models.AutoField(primary_key = True)
    title = models.CharField(max_length = 100)
    information = models.CharField(max_length = 400)
    class Meta:
        # managed = False
        db_table = 'information_tab'


'''
个人通知信息。
'''
class person_inform_tab(models.Model):
    personInfId = models.AutoField(primary_key = True)
    user_id = models.IntegerField()
    title = models.CharField(max_length = 100)
    information = models.CharField(max_length = 400)
    class Meta:
        # managed = False
        db_table = 'person_inform_tab'
    


'''
用于记录学者简介
若简介过长，next_id记录了下一个简介表项的sbf_id.
注：第一项的user_id为对应学者的user_id。 
'''
class scholar_brief_intro_tab(models.Model):
    sbf_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    brief = models.CharField(max_length = 100)
    number = models.IntegerField()              #表示是简介中的第几段,从1开始
    next_id = models.IntegerField(default = 0)   #下一段简介的sbf_id
    class Meta:
        # managed = False
        db_table = 'scholar_brief_intro_tab'




'''
学者学院关联表
'''
class scholar_department_tab(models.Model):
    id = models.AutoField(primary_key=True)
    scholar_id = models.IntegerField()      #学者id
    d_id = models.IntegerField()            #学院id

    class Meta:
        db_table = 'scholar_department_tab'


'''
举报信息表
'''
class report_tab(models.Model):
    r_id = models.AutoField(primary_key=True)#主码
    typeR = models.IntegerField(default = 0) #如果是0 的话举报的是人，1举报的是成果
    id = models.IntegerField()               #举报人的id
    a_id = models.IntegerField()             #被举报的id， 0：scholar_id人， 1：成果a_id
    user_name = models.CharField(max_length=100)  #0被举报人姓名/1被举报成果名称
    information = models.CharField(max_length=300)#用户填写的举报信息。
    flag = models.IntegerField()                  #管理员是否通过  

    class Meta:
        # managed = False
        db_table = 'report_tab'



'''
用户信息表
第一次使用时自动生成
'''
class user_tab(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=30) #学生昵称（微信名）
    wechatid = models.CharField(max_length=30)
    authority_choice = (
        (0, "普通用户"),
        (1, "学者用户"),
        (2, "学生用户")
    )
    authority = models.SmallIntegerField(choices=authority_choice,default=0)
    class Meta:
        # managed = False
        db_table = 'user_tab'

'''
学生的信息，
学生所在的学院见关联表 student_department_tab
'''
class student_tab(models.Model):
    user_id = models.IntegerField()
    student_id = models.AutoField(primary_key=True) #学生id
    school = models.CharField(max_length=30) #学校
    sno = models.CharField(max_length=30)    #学号
    name = models.CharField(max_length=30)  #学生姓名
    email = models.EmailField(max_length=30)#邮箱
    class Meta:
        # managed = False
        db_table = 'student_tab'

'''
class stuachievement_tab(models.Model):
    a_id = models.AutoField(primary_key=True)  # 主键，标识id
    name = models.CharField(max_length=150)  # 成果名
    year = models.CharField(max_length=5)  # 成果年份
    author_name = models.CharField(max_length=150)  # 作者名
    citation = models.IntegerField(default=-1)  # 被引数,若未爬到数据设为-1
    j_a_name = models.CharField(max_length=150)  # 成果出处
    file = models.CharField(max_length=150)  # 文件在服务器中的位置， 没有时为null
    link = models.CharField(max_length=150)  # 文件链接（只保留一个）
    kind = models.CharField(max_length=10)  # 文献类型
    num_view = models.IntegerField(default=0)  # 浏览次数
    get_id = models.IntegerField(default=0)  # 在原系统中的id,用于关联
    brief = models.IntegerField(default=0)  # 记录简介的第一项在AchieveBreif里的id

    keyword = models.CharField(max_length=200, default="NULL")

    class Meta:
        # managed = False
        db_table = 'stuachievement_tab'


class student_achievement_tab(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.IntegerField()
    a_id = models.IntegerField()
    class Meta:
        # managed = False
        db_table = 'student_achievement_tab'
'''

'''
学生与学院的关联表
'''
class student_department_tab(models.Model):
    sd_id = models.AutoField(primary_key=True) #主键
    student_id = models.IntegerField()
    d_id = models.IntegerField()
    class Meta:
        db_table = 'student_department_tab'



'''
用户的认证信息
'''
class authen_tab(models.Model):
    authen_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=30)
    name = models.CharField(max_length=30)
    sno = models.CharField(max_length=30)  #学号
    school = models.CharField(max_length = 30) #学校
    department = models.IntegerField() #学院对应的id
    identity_choice = (
        (0, "普通用户"),
        (1, "学者用户"),
        (2, "学生用户")
    )
    identity = models.SmallIntegerField(choices=identity_choice)
    class Meta:
        # managed = False
        db_table = 'authen_tab'

'''
用户与认证的关联表
'''
class user_authen_tab(models.Model):
#    u_id = models.AutoField(primary_key=True)
    authen_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()

    class Meta:
        # unique_together = ("authen_id","user_id")
        db_table = 'user_authen_tab'



'''
成果收藏表
'''
class collect_achievement_tab(models.Model):
    id = models.AutoField(primary_key = True)
    user_id = models.IntegerField()
    a_id = models.IntegerField()
   
    class Meta:
        # managed = False
        db_table = 'collect_achievement_tab' 

'''
学者收藏表
'''
class collect_scholar_tab(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    scholar_id = models.IntegerField()

    class Meta:
        # managed = False
        db_table = 'collect_scholar_tab'
        
'''
研究方向
'''
class reserch_direction_tab(models.Model):
    researchd_id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 30)
    class Meta:
        # managed = False
        db_table = 'reserch_direction_tab'
    
'''
研究方向与学者的关联表
'''
class scholar_direction_tab(models.Model):
    schReseaid = models.AutoField(primary_key = True)
    scholar_id = models.IntegerField()
    researchd_id = models.IntegerField()
    class Meta:
        # managed = False
        db_table = 'scholar_direction_tab'
    
    
'''
用于学者认领成果的表
'''    
class new_relation_tab(models.Model):
    a_id = models.AutoField(primary_key=True)
    auth_id = models.IntegerField(default=0)
    ach_id = models.IntegerField(default=0)

    class Meta:
        # managed = False
        db_table = 'new_relation_tab'
        

    
    
    
    
    
    
    
    
    
