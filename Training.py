import time
import math
import pyttsx
from chatterbot import ChatBot

AI_Bot = ChatBot("Scofield",
              trainer="chatterbot.trainers.ChatterBotCorpusTrainer",
              storage_adapter="chatterbot.adapters.storage.MongoDatabaseAdapter",
              io_adapters=[
                  "chatterbot.adapters.io.TerminalAdapter"
              ],
              database="scofield")

engine=pyttsx.init()
engine.setProperty('rate', 180)# words per minute

print "AI Bot Training Initiated."

engine.say("AI Bot Training Initiated.")
engine.runAndWait()

start=time.time()

AI_Bot.train("chatterbot.corpus")

end=time.time()

total_time=round(end-start,2);

answer="AI Bot trained successfully in " + str(total_time) + " seconds";
print answer

engine.say(answer)
engine.runAndWait()

time.sleep(2)
