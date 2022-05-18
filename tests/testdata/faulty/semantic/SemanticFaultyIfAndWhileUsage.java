class A {
    public static void main(String[] args){
		    System.out.println(new B().oneMethod());
    }
}

class B {

    public int oneMethod(){
        int intArg;

        intArg = 1;

        if (intArg * 2) System.out.println(1) ;
        else System.out.println(0) ;

        while (intArg * 2) System.out.println(1) ;
	    
        return 0 ;
    }
}