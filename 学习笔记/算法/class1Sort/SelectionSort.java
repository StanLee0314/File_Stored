package basic_class_01;

//选择排序
public class SelectionSort {
    public  static int[] swap(int[] a,int i , int  j ){
        int temp = a[i];
         a[i] = a[j];
        a[j] = temp;
   return  a;
    }

    public static int[] sortMethod(int[] a){
        if(a == null || a.length <2 )
            return a;
        for ( int start = 0 ; start < a.length ; start ++){
            int minIndex = start;
            for (int j = start ; j < a.length ; j++ ){
                minIndex = a[minIndex]<a[j]? minIndex:j;
            }
            swap(a, minIndex, start);
        }

        return a;
    }
    public static void main(String[] args) {
        int [] a= {1,2,3,334,5,63,32,2,34,4};
        int[] b = sortMethod(a);
        for (int num:b){
            System.out.print(num + ",");
        }
    }
    }

