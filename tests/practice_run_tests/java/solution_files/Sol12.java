package tests.practice_run_tests.java.solution_files;

public class Sol12 {
  public static int solve(double num, double[] arr) {
    double ret = num;
    for (double d : arr) {
      ret += d;
    }
    return (int) ret;
  }
}
