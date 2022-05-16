class A {
    public static void main(String[] args){
		System.out.println(new B().oneMethod(20));
    }
}

class B {

    public int oneMethod(int param){
		boolean a;
		int b;
		a = a && b;
		b = a + b;
		b = a - b;
		b = a * b;
		b = a < b;

		return param ;
    }

}