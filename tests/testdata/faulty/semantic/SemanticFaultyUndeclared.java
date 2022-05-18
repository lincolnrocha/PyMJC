class A {
    public static void main(String[] args){
		    System.out.println(new B().oneMethod());
    }
}

class B extends D {

    public int oneMethod(){
        obj = 0;
		    return 0;
    }

    public int otherMethod(){
        C obj1;
        B obj2;
        obj1 = new C();
        obj2 = new B();
        System.out.println(obj2.twoMethod());
		return 0;
    }

}