from django.test import TestCase
from .models import *
from .scheduled_content import *
from django.db import connection
import time
from django.core.management import call_command

# Create your tests here.
class ScheduledMessagesTestControl(TestCase):
    def setUp(self):
        default_arm, created = Arm.objects.get_or_create(name="ai_chat")
                
        if created:
            print("created arm")
        phone_number_instance = PhoneNumber(phone_number='17204001070', arm=default_arm,name="Joshua",opted_in=True,
                                            pre_survey='www.google.com',post_survey='www.google.com')
        phone_number_instance.save()
        print("created phone number")

        call_command('loaddata', 'base/fixtures/topics_fixture.json')
        call_command('loaddata', 'base/fixtures/scheduledmessage_fixture.json')
        call_command('loaddata', 'base/fixtures/scheduledmessagecontrol_fixture.json')
        call_command('loaddata', 'base/fixtures/topicgoals_fixture.json')
    
    def dummy_test(self):
        self.assertEqual(1, 1)
        
    def test_scheduled_messages(self):
        for day in range(1, 31):
            with connection.cursor() as cursor:
                cursor.execute("UPDATE base_phonenumber SET created_at = created_at - INTERVAL '1 day'")
            print("Day " + str(day))
            #time.sleep(1)
            send_topic_selection_message()
            #time.sleep(1)
            print("topic selection message sent")
            send_scheduled_message()
            #time.sleep(1)
            print("scheduled message sent")
            send_goal_message()
            #time.sleep(1)
            print("goal message sent")
            send_goal_feedback()
            #time.sleep(1)
            print("goal feedback sent")
            send_final_pilot_message()
            #time.sleep(1)
            print("final pilot message sent")

