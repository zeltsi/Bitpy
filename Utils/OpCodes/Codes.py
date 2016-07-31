import Utils.keyUtils.keys

class Stack():

    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        elm = self.items.pop()
        return elm

    def size(self):
        return len(self.items)

    def printStack(self):
        display = ""
        for items in self.items:
            items = str(items)
            if len(items) > 5:
                display += " " + "<"+ items[:5] + "..." + ">"
            else:
                display += " " + "<" + items + ">"
        return display

    def clear(self):
        self.items.clear()

    def OP_DUP(self):
        elm = self.pop()
        self.items.append(elm)
        self.items.append(elm)

    def OP_HASH160(self): #saved as string!
        self.push(Utils.keyUtils.keys.generate_hashed_public_key_string(self.pop()))

    def OP_EQUAL(self):
        elm1 = self.pop()
        elm2 = self.pop()

        if elm1 == elm2:
            self.push(1)
        else:
            self.push(0)

    def OP_VERIFY(self):
        top = self.pop()
        if top == 1:
            self.push(1)
        else:
            self.push(0)

    def OP_RETURN(self, input):
        self.push(input)




