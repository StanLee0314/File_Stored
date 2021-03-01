package basic_class_01;

public class HeapSort {
    //一个节点进来只需要和层数相比较进行交换O（logN)
    public static void heapInsert(int[] arr, int i){
      while (arr[i] > arr[(i-1)/2]){
//          int index = i;
          swap(arr, i , (i-1)/2);
          i = (i-1)/2;
        }
    }

    //堆在数组上 0 - heapSise-1 上为大根堆
    //index 上位置变小了， 然后自平衡
    public static void heapify(int[] arr, int index, int heapSize){
        int left = index*2 +1;
        while (left <heapSize){
            int larger = left +1 < heapSize && arr[left +1] > arr[left]?
                    left+1:left;
            larger = arr[larger] >arr[index]? larger:index;
            if(larger == index){
                break;
            }
            //larger!= index
            swap(arr,index,larger);
            index =larger;
            left = index*2 +1;
        }
    }
    public static void heapSort(int[] arr){
        if(arr == null || arr.length <2){
            return;
        }
        for(int i = 0;i< arr.length;i++){
            heapInsert(arr,i);
        }
        int heapSize = arr.length;
        swap(arr,--heapSize,0);

       while (heapSize>0){
        heapify(arr,0,heapSize);
        heapSize--;
        swap(arr,0,heapSize);

        }


    }
    public static int[] generateRandomArray(int maxSize, int maxValue) {
        int[] arr = new int[(int) ((maxSize + 1) * Math.random())];
        for (int i = 0; i < arr.length; i++) {
            arr[i] = (int) ((maxValue + 1) * Math.random()) - (int) (maxValue * Math.random());
        }
        return arr;
    }
    public static void main(String[] args) {
        int[] arr = generateRandomArray(20, 20);
        printArray(arr);
        heapSort(arr);
        printArray(arr);
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
    public static void swap(int[] arr, int i, int j) {
        int tmp = arr[i];
        arr[i] = arr[j];
        arr[j] = tmp;
    }
}
