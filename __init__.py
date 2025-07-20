#━━━━━━━━━━━━━━━━━━━━━━
#     Load Modules     
#━━━━━━━━━━━━━━━━━━━━━━

from . import rec_oriorient

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#     Register & Unregister     
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def register():
    rec_oriorient.register()

def unregister():
    rec_oriorient.unregister()

if __name__ == "__main__":
    register() 