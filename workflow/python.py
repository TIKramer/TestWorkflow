from fireworks import *
from fireworks.core.rocket_launcher import rapidfire
from fireworks.flask_site.app import app

# set up the LaunchPad and reset it
launchpad = LaunchPad()
launchpad.reset('', require_password=False)

# define five individual FireWorks used in the Workflow
task1 = ScriptTask.from_str('echo "Hello I am task one."')
task2 = ScriptTask.from_str('echo "Hello I am task two I wait on task 1."')
task3 = ScriptTask.from_str('echo "Hello I am task three. I wait on task 1."')
task4 = ScriptTask.from_str('echo "Hello I am task four. I wait on task 3"')
task5 = ScriptTask.from_str('echo "Hello I am task five I wait on task 4"')

fw1 = Firework(task1, fw_id=1, name='Task 1')
fw2 = Firework(task2, name='Task2')
fw3 = Firework(task3, name = 'Task3')
fw4 = Firework(task4, name='Task4')
fw5 = Firework(task5, name='Task5')


# assemble Workflow from FireWorks and their connections by id
# f2 and f3 wait on f1
# f4 waits on f2 
#f4 waits on f3
workflow = Workflow([fw1, fw2, fw3, fw4, fw5], {fw1: [fw2, fw3], fw2: [fw4], fw3: [fw4], fw4: [fw5]})

# store workflow and launch it locally
launchpad.add_wf(workflow)
rapidfire(launchpad, FWorker())


app.lp = launchpad  # change launchpad to the one you one to display - one Im using is defined at line 6
app.config["WEBGUI_USERNAME"] = "admin"  
app.config["WEBGUI_PASSWORD"] = "admin"  
app.run(debug=True)