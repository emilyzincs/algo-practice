package tests.practice_run_tests.java.solution_files;

public class Sol12 {
  public static long solve(double num, double[] arr) {
    double ret = num;
    for (double d : arr) {
      ret += d;
    }
    return (long) ret;
  }
}
