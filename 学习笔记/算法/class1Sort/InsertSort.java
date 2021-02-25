package basic_class_01;

//插入排序
public class InsertSort {
    public static int[] sortMethod(int[] a ){
        if (a ==null || a.length < 2){
            return a;
        }
        for(int start = 1; start < a.length ;start ++) {
            for (int num  = start-1; num >= 0 && a[num] > a[num+1];num --){
                    swap(a,num,num +1);
            }
        }
        return a;
    }
    public  static int[] swap(int[] a,int i , int  j ) {
        int temp = a[i];
        a[i] = a[j];
        a[j] = temp;
        return a;

    }
    public static void main(String[] args) {
        int [] a= {1,2,333,4,5,63,32,2,34,4};
        int[] b = sortMethod(a);
        for (int num:b){
            System.out.print(num + ",");
        }
    }

}
