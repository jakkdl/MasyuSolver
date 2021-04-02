# This is a test file for how merging works

def workArea1():
    print("Entering workArea1()")
    print("\tFred's initial work in workArea1()")
    print("Leaving workArea1()")

def newMethod():
    print("Just another method")

def newMethod2():
    print("Just another method")

def workArea2():
    print("Entering workArea2()")
    print("\tFred's initial work in workArea2()")
    print("Leaving workArea2()")

def nonConflictingMerge():
    print("This should be a non-conflicting merge!")

# This block is a non-conflicting change
def workArea3():
    print("Entering workArea3()")
    print("\tFred's initial work in workArea3()")
    print("Leaving workArea3()")

if __name__ == "__main__":
    workArea1()
    workArea2()
    # This is probably a conflicting merge .. will have to be manually dealt with
    nonConflictingMerge()
    workArea3()  # Conflicting change
    # Just adding a comment
    # Just another comment