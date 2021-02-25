package basic_class_01;

public class SmallSum {
    public static void smallSum(int[] arrs){
        if(arrs == null || arrs.length<2){
            return ;
        }
        smallSum(arrs,0,arrs.length-1);
    }

    public static void smallSum(int[] arrs, int l, int r){
        if(l == r){
            return ;
        }
        int mid = l + ((r - l)>>1);
        smallSum(arrs, l, mid);
        smallSum(arrs, mid +1, r);
        numMerge(arrs , l ,r );
    }

//    public static int merge(int[] arr, int l, int m, int r) {
//        int[] help = new int[r - l + 1];
//        int i = 0;
//        int p1 = l;
//        int p2 = m + 1;
//        int res = 0;
//        while (p1 <= m && p2 <= r) {
//            res += arr[p1] < arr[p2] ? (r - p2 + 1) * arr[p1] : 0;
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
//        return res;
//    }


    public static  int merge(int[] arrs, int l, int r){
        int mid = l + ((r - l )>>1);
        int i = 0;
        int[] help =new int[r - l +1];
        int p1 = l;
        int p2 = mid +1;
        int res = 0;
        while (p1 <= mid && p2 <= r){
            res += arrs[p1] < arrs[p2] ? (r - p2 + 1) * arrs[p1] : 0; //重点
            help[i++] = arrs[p1] < arrs [p2]? arrs[p1++]: arrs[p2++];
        }
        while(p1 <= mid){
            help[i++] = arrs[p1++];
        }
        while ((p2<= r)){
            help[i++] = arrs[p2++];
        }
        for ( i =0; i< help.length; i++){
            arrs[l+ i] = help[i];
        }
        return res;
    }
//逆序对 （如果左边的数比右边的大就打印）
public static void numMerge(int[] arrs, int l, int r){
    int mid = l + ((r - l )>>1);
    int i = 0;
    int[] help =new int[r - l +1];
    int p1 = l;
    int p2 = mid +1;
//    int res = 0;
    while (p1 <= mid && p2 <= r){
        if(arrs[p1] <arrs[p2]){
            for (int nums = p1 ; nums <= mid ;nums ++){
                System.out.println(arrs[nums] + "," + arrs[p2] + " ");
            }
        }

        help[i++] = arrs[p1] > arrs [p2]? arrs[p1++]: arrs[p2++];
    }
    while(p1 <= mid){
        help[i++] = arrs[p1++];
    }
    while ((p2<= r)){
        help[i++] = arrs[p2++];
    }
    for ( i =0; i< help.length; i++){
        arrs[l+ i] = help[i];
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
    public static void main(String[] args) {
       int[] a = {1,3,4,2,5};
       smallSum(a);
//       printArray(a);
    }
}
