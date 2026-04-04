package tests.java.solution_files;

public class Sol12 {
  public static long solve(double f, double[] a) {
    double ret = f;
    for (double d : a) {
      ret += d;
    }
    return (long) ret;
  }
}
