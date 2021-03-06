import sys
import traceback
sys.path.append("./lib/")
import Utility

commands = ["!help", "!botstats", "!cmods", "!cscheds", "!umod", "!lmod", "!reboot"]

class AdvControl:
	
	def __init__(self, eng):
		self.type = "PRIVMSG"
		self.name = "advctrl"
		self.engine = eng
		self.func = Utility.Misc()

	def message(self, bot, who, location, message, args):
		rights = self.engine.get_access().get_user_rights(who, bot)
		if (rights < 0): # Trusted Commands and Above (1+)
			return
		cmd = args[0].lower()
		
		if cmd == "!help":
			return bot.notice(who[0], "Advanced Control help: " + ", ".join(commands))
		
		if cmd == "!botstats":
			return bot.message(location, "BotsConnected: " + str(len(self.engine.get_bots())) + " - " +
						"ModsLoaded: " + str(len(self.engine.event.mods)) + " - " + 
						"SchedLoaded: " + str(len(self.engine.sched.evt)))
						
		if cmd == "!cmods":
			return bot.message(location, "LoadedMods: " + ", ".join(self.engine.event.get_list()))
			
		if cmd == "!cscheds":
			return bot.message(location, "LoadedSchedules: " + ", ".join(self.engine.sched.get_list()))
			
		if (rights < 1):
			return
			
		if cmd == "!umod" and len(args) > 1:
			if self.engine.event.unload(args[1]):
				return bot.message(location, "Unloaded module " + args[1])
			else:
				return bot.message(location, "Unable to remove module " + args[1])

		if cmd == "!lmod" and len(args) > 1:
			if self.engine.event.reload(args[1]):
				return bot.message(location, "Reloaded module " + args[1])
			else:
				return bot.message(location, "Unable to reload module " + args[1])
				
		if cmd == "!reboot":
			if len(args) > 1 and args[1].lower() == "confirm":
				bot.message(location, "Going down now!")
				self.engine.log.write("Confirmed shutdown by " + who[0] + " on " + bot.network.name)
				return self.engine.shutdown(bot, immediate=True)
			else:
				self.engine.log.write("Shutdown by " + who[0] + " on " + bot.network.name)
				bot.message(location, "Good-bye!")
				return self.engine.shutdown(bot)
				
