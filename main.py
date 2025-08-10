from src import Control, Model, View

def main():
    model = Model()
    view = View()

    ctrl = Control(model, view)

if __name__ == "__main__":
    main()