import argparse


class Run:
    __parser = argparse.ArgumentParser(prog='Simple CPU instruction set simulator',
                                     description='Simple CPU instruction set simulator is a teaching tool showing how a CPU operates and assembly is executed')

    def __init__(self):
        simulator_presenting_group = self.__parser.add_mutually_exclusive_group()
        simulator_presenting_group.add_argument("-cli", "--cli-simulator", help="Selecting command line simulator",
                                              action='store_true')
        simulator_presenting_group.add_argument("-gui", "--gui-simulator", help="Selecting graphical simulator",
                                              action='store_true')

        args = self.__parser.parse_args()


if __name__ == '__main__':
    Run()