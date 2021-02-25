package basic_class_01;

public class Helanguoqi {

//返回等于数组的左右边界数组 两个值
    public static void partition(int[] arr, int l, int r, int num) {
        int less = l - 1;
        int more = r + 1;
        int cur = l;
        while (cur < more) {
            if (arr[cur] < num) {
                less++;
                swap(arr, less, cur);
                cur++;
            } else if (arr[cur] > num) {
                more--;
                swap(arr, cur, more);
            } else if (arr[cur] == num) {
                cur++;
            }

        }

    }

        public static int[] partition(int[] arr, int l, int r){
            int less = l-1;
            int more = r +1;
            int cur = l;
            while(cur <more){
                if(arr[cur]<arr[r]){
                    less++;
                    swap(arr, less, cur);
                    cur++;
                }else if(arr[cur]> arr[r]){
                    more --;
                    swap(arr,cur,more);
                }else if(arr[cur] == arr[r]){
                    cur ++;
                }
            }
        return new int[]{less,more};
    }

    public static void swap(int[] arr, int l, int r){
        int temp = arr[l];
        arr[l] = arr [r];
        arr[r] = temp;
    }




public static void quicksort(int[] arr, int l , int r) {
    if (l < r) {
        int[] p = partition(arr, l, r);
        quicksort(arr, l, p[0]);
        quicksort(arr, p[1], r);

    }
}
    public static void main(String[] args) {
      int[] a = {2,3,54,63,2,5,6,6,6,354,1};
      int num = 6;
//      partition(a,0,a.length-1,num);
     quicksort(a,0,a.length-1);
      for(int c:a){
          System.out.print(c + ",");
      }
    }
}
