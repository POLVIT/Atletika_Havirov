from django_cron import CronJobBase, Schedule
from mediator.models import createPost
from datetime import datetime
import os
ig_name=os.environ.get('ig_name')
ig_pass=os.environ.get('ig_pass')
#fb


#ig
from myigbot import MyIGBot



class SocialMediaJob(CronJobBase):
    RUN_EVERY_MINS = 5

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'Atletika_Havirov/jobs'    # a unique code

    def do(self):
        ####################  WEB #########################
        web_posty = createPost.objects.filter(web_post=True).filter(web_post_succes=False)
        for w in web_posty:
            #dopln
            w.web_post_succes=True
        ####################  FB #########################
        fb_posty = createPost.objects.filter(fb_time__lt=datetime.now()).filter(fb_post=False)
        for fb in fb_posty:
            #dopln
            fb.fb_post=True
        ####################  IG #########################
        ig_posty = createPost.objects.filter(ig_time__lt=datetime.now()).filter(ig_post=False)
        for ig in ig_posty:
            bot = MyIGBot(ig_name,ig_pass)
            p = ig.foto_urls
            forbiden = ["[", "]", "'", '"']
            for f in forbiden: p = p.replace(f, '')
            bot.upload_post(f'{p.split(",")[0]}',ig.text)
            ig.ig_post = True