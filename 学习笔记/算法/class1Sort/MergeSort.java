package basic_class_01;

public class MergeSort {

    public static void mergeSort(int[] arr) {
        if (arr == null || arr.length < 2) {
            return;
        }
        mergeSort(arr, 0, arr.length - 1);
    }


    public static void mergeSort(int[] arr, int L, int R){
        if(L==R)
            return;
        int mid = (L+R)/2;
        mergeSort(arr, L, mid);
        mergeSort(arr, mid+1, R);
//        merge(arr,L,R);

        merge(arr, L, R);
    }



//    public static void merge(int[] arr, int l, int m, int r) {
//        int[] help = new int[r - l + 1];
//        int i = 0;
//        int p1 = l;
//        int p2 = m + 1;
//        while (p1 <= m && p2 <= r) {
//            help[i++] = arr[p1] < arr[p2] ? arr[p1++] : arr[p2++];
//        }
//        while (p1 <= m) {
//            help[i++] = arr[p1++];
//        }
//        while (p2 <= r) {
//            help[i++] = arr[p2++];
//        }
//        for (i = 0; i < help.length; i++) {
//            arr[l + i] = help[i];
//        }
//    }



    public static void merge(int[] arr, int L,  int R){
        int[] help = new int[R-L+1];
        int i =0;
        int p = L;
        int mid = (L + R)/2;
        int q = mid +1;
        while (p <= mid && q <= R){
            help[i++] = arr[p] < arr[q]? arr[p++] : arr[q++];
        }
        while(p<=mid){
            help[i++] = arr[p++];
        }
        while(q<=R){
            help[i++] = arr[q++];
        }
        for(int temp = 0; temp< help.length;temp ++){
            arr[L + temp] =help[temp];
        }
    }

    public static void printArray(int[] arr) {
        if (arr == null) {
            return;
        }
        for (int i = 0; i < arr.length; i++) {
            System.out.print(arr[i] + " ");
        }
        System.out.println();
    }

    public static int[] generateRandomArray(int maxSize, int maxValue) {
        int[] arr = new int[(int) ((maxSize + 1) * Math.random())];
        for (int i = 0; i < arr.length; i++) {
            arr[i] = (int) ((maxValue + 1) * Math.random()) - (int) (maxValue * Math.random());
        }
        return arr;
    }


    public static void main(String[] args) {
       int[] a=generateRandomArray(20,20);
        printArray(a);
        mergeSort(a,0,a.length -1);
        printArray(a);
    }
}
