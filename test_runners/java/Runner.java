package test_runners.java;

import com.fasterxml.jackson.databind.ObjectMapper;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.lang.reflect.Method;
import java.util.*;

public class Runner {
  private static Method refMethod;
  private static Method userMethod;
  private static final ObjectMapper mapper = new ObjectMapper();

  public static void main(String[] args) throws Exception {
    if (args.length != 2) {
      System.err.println("Usage: java Runner <problem name> <test.json>");
      System.exit(1);
    }
    String problemName = args[0];
    String testFile = args[1];

    // Load reference and user classes
    Class<?> refClass = Class.forName("problems." + problemName + ".Solution");
    refMethod = findSolveMethod(refClass);
    Class<?> userClass = Class.forName("practice.Attempt");
    userMethod = findSolveMethod(userClass);
    checkMethodCompatibility();

    // Parse JSON
    Map<String, Object> root = mapper.readValue(Files.readAllBytes(Paths.get(testFile)), Map.class);
    List<Map<String, Object>> tests = (List<Map<String, Object>>) root.get("tests");

    for (Map<String, Object> test : tests) {
      int number = (int) test.get("number");
      Object expected = test.get("expected");
      List<?> inputs = (List<?>) test.get("inputs");

      Object actual = invokeUserMethod(inputs);
      if (!actual.equals(expected)) {
        System.err
            .println("Test " + number + " failed: expected " + expected + " but got " + actual);
        System.exit(1);
      }
    }
    System.out.println("All tests passed");
  }

  private static Method findSolveMethod(Class<?> clazz) {
    for (Method m : clazz.getDeclaredMethods()) {
      if (m.getName().equals("solve") && java.lang.reflect.Modifier.isStatic(m.getModifiers())) {
        return m;
      }
    }
    throw new RuntimeException("No static solve method found in " + clazz.getName());
  }

  private static void checkMethodCompatibility() {
    Class<?>[] refParams = refMethod.getParameterTypes();
    Class<?>[] userParams = userMethod.getParameterTypes();

    if (refParams.length != userParams.length) {
      throw new RuntimeException("Parameter count mismatch: reference expects " + refParams.length
          + ", user method has " + userParams.length);
    }

    for (int i = 0; i < refParams.length; i++) {
      if (!refParams[i].equals(userParams[i])) {
        throw new RuntimeException("Parameter type mismatch at index " + i + ": reference expects "
            + refParams[i].getName() + ", user method has " + userParams[i].getName());
      }
    }
  }

  private static Object invokeUserMethod(List<?> inputs) throws Exception {
    Class<?>[] paramTypes = refMethod.getParameterTypes();
    if (paramTypes.length != inputs.size()) {
      throw new IllegalArgumentException("Number of inputs does not match method parameters");
    }

    // Convert each input to the expected parameter type
    Object[] args = new Object[paramTypes.length];
    for (int i = 0; i < paramTypes.length; i++) {
      args[i] = mapper.convertValue(inputs.get(i), paramTypes[i]);
    }

    return userMethod.invoke(null, args);
  }
}
