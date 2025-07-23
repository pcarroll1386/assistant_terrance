class CharLCD1602(object):
    def __init__(self):
        pass

    def clear(self):
        """This is a mock up of the LCD1062 clear function.
        It does not perform any actual operation since this is a mock class.
        """
        pass

    def destroy(self):
        self.clear()

    def write(self,x, y, str):
        print(str)
    

