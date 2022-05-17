class A {
    public static void main(String[] args){
		System.out.println(new B().oneMethod());
    }
}

class B {

    public int oneMethod(){
      int[] aux1;
      int aux2;
      int[] aux3;
      int aux4;
      boolean value;

      value = true;
      aux1 = new int[3];
      aux1[0] = value;
      aux4 = aux1[value];
      aux4 = aux2[0];
      aux4 = aux2.length;
      aux3 = new int[value];

		  return 0 ;
    }

}