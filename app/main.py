from root import Root
import subprocess
import sys

def atualizar_aplicativo():
    subprocess.run([sys.executable, 'update.py'])
    
if __name__ == '__main__':
    app = Root()
    app.mainloop()