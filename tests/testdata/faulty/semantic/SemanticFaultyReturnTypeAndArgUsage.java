class A {
    public static void main(String[] args){
        {
            System.out.println(new B().oneMethod(20));
            System.out.println(new B().threeMethod(20,10));
        }
    }
}

class B {

    public int oneMethod(boolean param){
		return param ;
    }

    public int twoMethod(boolean param, boolean paramB, boolean paramB){
		return param ;
    }

    public int threeMethod(int param01, int param02, int param03){
		return param01 ;
    }
}