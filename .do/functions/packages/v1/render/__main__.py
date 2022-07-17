# import ancv
import os
import sys

def main(args):
    name = args.get("name", "stranger")
    greeting = "Hello " + name + "!"
    print(greeting)
    return {"body": str({"env": os.environ, "id": os.getuid(), "path": str(sys.path)})}
