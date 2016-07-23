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

    def OP_DUP(self):
        elm = self.pop()
        self.items.append(elm)
        self.items.append(elm)

    def OP_HASH160(self): #saved as string!
        self.push(str(Utils.keyUtils.keys.generate_hashed_public_key(self.pop())))

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



s = Stack()
s.push("sig")
s.push("0408858B4D43333192C79A361B8766357A795037F213BEE7D82268312E45DBA0C73F3EB2D481FE92FA157A724A001E91BF4858C9C6E99620BB4FDDEBEC51AB5633")
s.OP_DUP()

s.OP_HASH160()


s.push(b'478075922af41fb441aa0ab67e91aef27ef1e686')
s.OP_EQUAL()


