package test_runners.java;

import com.fasterxml.jackson.databind.ObjectMapper;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.lang.reflect.Field;
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

    // Load reference class and get its method (any static solve)
    Class<?> refClass = Class.forName("problems." + problemName + ".Solution");
    refMethod = findSolveMethod(refClass);

    // Load user class and find method matching reference's parameter types
    Class<?> userClass = Class.forName("practice.Attempt");
    userMethod = findSolveMethod(userClass, refMethod.getParameterTypes());
    checkMethodCompatibility();

    // Parse JSON
    Map<String, Object> root = mapper.readValue(Files.readAllBytes(Paths.get(testFile)), Map.class);
    String answerAmount = (String) root.get("answer_amount");
    if (!"single".equals(answerAmount) && !"multiple".equals(answerAmount)) {
      throw new IllegalStateException("Json test file does not contain valid answerAmount field");
    }
    boolean uniqueAnswer = answerAmount.equals("single");
    List<Map<String, Object>> tests = (List<Map<String, Object>>) root.get("tests");

    for (int i = 0; i < tests.size(); i++) {
      Map<String, Object> test = tests.get(i);
      List<?> inputs = (List<?>) test.get("inputs");
      Object actual = invokeUserMethod(inputs);
      boolean error = false;

      if (uniqueAnswer) {
        Object expected = test.get("expected");
        if (!deepEquals(actual, expected)) {
          error = true;
        }
      } else {
        List<?> expected = (List<?>) test.get("expected");
        if (!inList(actual, expected)) {
          error = true;
        }
      }

      if (error) {
        String actualAsString = deepToString(actual);
        String optionalPart = actualAsString.length() <= 100 ? " Value: " + actualAsString : "";
        System.err.println("Test " + (i + 1) + " failed." + optionalPart);
        System.exit(1);
      }
    }
    System.out.println("All tests passed");
  }

  private static Method findSolveMethod(Class<?> clazz) {
    // For reference class, any static solve is fine (assume only one)
    for (Method m : clazz.getDeclaredMethods()) {
      if (m.getName().equals("solve") && java.lang.reflect.Modifier.isStatic(m.getModifiers())) {
        return m;
      }
    }
    throw new RuntimeException("No static solve method found in " + clazz.getName());
  }

  private static Method findSolveMethod(Class<?> clazz, Class<?>[] paramTypes) {
    // For user class, find method with exact parameter types
    for (Method m : clazz.getDeclaredMethods()) {
      if (m.getName().equals("solve") && java.lang.reflect.Modifier.isStatic(m.getModifiers())
          && Arrays.equals(m.getParameterTypes(), paramTypes)) {
        return m;
      }
    }
    throw new RuntimeException("No static solve method with signature "
        + Arrays.toString(paramTypes) + " found in " + clazz.getName());
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

    Object[] args = new Object[paramTypes.length];
    for (int i = 0; i < paramTypes.length; i++) {
      args[i] = mapper.convertValue(inputs.get(i), paramTypes[i]);
    }

    return userMethod.invoke(null, args);
  }

  private static boolean inList(Object obj, List<?> list) {
    for (Object other : list) {
      if (deepEquals(obj, other)) {
        return true;
      }
    }
    return false;
  }

  // ========== Deep Equality ==========

  private static boolean deepEquals(Object a, Object b) {
    if (a == b)
      return true;
    if (a == null || b == null)
      return false;

    // Arrays
    if (a.getClass().isArray() && b.getClass().isArray()) {
      return deepArraysEquals(a, b);
    }

    // Collections
    if (a instanceof Collection && b instanceof Collection) {
      Collection<?> colA = (Collection<?>) a;
      Collection<?> colB = (Collection<?>) b;
      if (colA.size() != colB.size())
        return false;
      Iterator<?> itA = colA.iterator();
      Iterator<?> itB = colB.iterator();
      while (itA.hasNext()) {
        if (!deepEquals(itA.next(), itB.next()))
          return false;
      }
      return true;
    }

    // Maps
    if (a instanceof Map && b instanceof Map) {
      Map<?, ?> mapA = (Map<?, ?>) a;
      Map<?, ?> mapB = (Map<?, ?>) b;
      if (mapA.size() != mapB.size())
        return false;
      for (Object key : mapA.keySet()) {
        if (!mapB.containsKey(key))
          return false;
        if (!deepEquals(mapA.get(key), mapB.get(key)))
          return false;
      }
      return true;
    }

    // Custom types: ListNode, TreeNode
    if (isListNode(a) && isListNode(b)) {
      try {
        return deepEqualsListNode(a, b);
      } catch (Exception e) {
        throw new RuntimeException("Failed to compare ListNode", e);
      }
    }
    if (isTreeNode(a) && isTreeNode(b)) {
      try {
        return deepEqualsTreeNode(a, b);
      } catch (Exception e) {
        throw new RuntimeException("Failed to compare TreeNode", e);
      }
    }

    // Default
    return a.equals(b);
  }

  private static boolean deepArraysEquals(Object a, Object b) {
    Class<?> compTypeA = a.getClass().getComponentType();
    Class<?> compTypeB = b.getClass().getComponentType();
    if (compTypeA != compTypeB)
      return false;

    if (compTypeA.isPrimitive()) {
      if (compTypeA == int.class)
        return Arrays.equals((int[]) a, (int[]) b);
      if (compTypeA == long.class)
        return Arrays.equals((long[]) a, (long[]) b);
      if (compTypeA == double.class)
        return Arrays.equals((double[]) a, (double[]) b);
      if (compTypeA == float.class)
        return Arrays.equals((float[]) a, (float[]) b);
      if (compTypeA == boolean.class)
        return Arrays.equals((boolean[]) a, (boolean[]) b);
      if (compTypeA == byte.class)
        return Arrays.equals((byte[]) a, (byte[]) b);
      if (compTypeA == char.class)
        return Arrays.equals((char[]) a, (char[]) b);
      if (compTypeA == short.class)
        return Arrays.equals((short[]) a, (short[]) b);
    } else {
      Object[] arrA = (Object[]) a;
      Object[] arrB = (Object[]) b;
      if (arrA.length != arrB.length)
        return false;
      for (int i = 0; i < arrA.length; i++) {
        if (!deepEquals(arrA[i], arrB[i]))
          return false;
      }
      return true;
    }
    return false;
  }

  private static boolean isListNode(Object obj) {
    return obj != null && obj.getClass().getName().endsWith(".ListNode");
  }

  private static boolean isTreeNode(Object obj) {
    return obj != null && obj.getClass().getName().endsWith(".TreeNode");
  }

  private static boolean deepEqualsListNode(Object a, Object b) throws Exception {
    Class<?> clazz = a.getClass();
    Field valField = clazz.getDeclaredField("val");
    valField.setAccessible(true);
    Field nextField = clazz.getDeclaredField("next");
    nextField.setAccessible(true);

    int valA = valField.getInt(a);
    int valB = valField.getInt(b);
    if (valA != valB)
      return false;

    Object nextA = nextField.get(a);
    Object nextB = nextField.get(b);
    return deepEquals(nextA, nextB);
  }

  private static boolean deepEqualsTreeNode(Object a, Object b) throws Exception {
    Class<?> clazz = a.getClass();
    Field valField = clazz.getDeclaredField("val");
    valField.setAccessible(true);
    Field leftField = clazz.getDeclaredField("left");
    leftField.setAccessible(true);
    Field rightField = clazz.getDeclaredField("right");
    rightField.setAccessible(true);

    int valA = valField.getInt(a);
    int valB = valField.getInt(b);
    if (valA != valB)
      return false;

    Object leftA = leftField.get(a);
    Object leftB = leftField.get(b);
    if (!deepEquals(leftA, leftB))
      return false;

    Object rightA = rightField.get(a);
    Object rightB = rightField.get(b);
    return deepEquals(rightA, rightB);
  }

  // ========== String Representation ==========

  private static String deepToString(Object obj) {
    if (obj == null)
      return "null";
    if (obj.getClass().isArray()) {
      if (obj instanceof Object[]) {
        return Arrays.deepToString((Object[]) obj);
      } else {
        // primitive arrays
        if (obj instanceof int[])
          return Arrays.toString((int[]) obj);
        if (obj instanceof long[])
          return Arrays.toString((long[]) obj);
        if (obj instanceof double[])
          return Arrays.toString((double[]) obj);
        if (obj instanceof float[])
          return Arrays.toString((float[]) obj);
        if (obj instanceof boolean[])
          return Arrays.toString((boolean[]) obj);
        if (obj instanceof byte[])
          return Arrays.toString((byte[]) obj);
        if (obj instanceof char[])
          return Arrays.toString((char[]) obj);
        if (obj instanceof short[])
          return Arrays.toString((short[]) obj);
      }
    }
    if (isListNode(obj)) {
      return listNodeToString(obj);
    }
    if (isTreeNode(obj)) {
      return treeNodeToString(obj);
    }
    return obj.toString();
  }

  private static String listNodeToString(Object node) {
    StringBuilder sb = new StringBuilder("[");
    try {
      Class<?> clazz = node.getClass();
      Field valField = clazz.getDeclaredField("val");
      valField.setAccessible(true);
      Field nextField = clazz.getDeclaredField("next");
      nextField.setAccessible(true);

      Object cur = node;
      while (cur != null) {
        sb.append(valField.getInt(cur));
        cur = nextField.get(cur);
        if (cur != null)
          sb.append(",");
      }
    } catch (Exception e) {
      return node.toString(); // fallback
    }
    sb.append("]");
    return sb.toString();
  }

  private static String treeNodeToString(Object node) {
    if (node == null)
      return "null";
    try {
      Class<?> clazz = node.getClass();
      Field valField = clazz.getDeclaredField("val");
      valField.setAccessible(true);
      Field leftField = clazz.getDeclaredField("left");
      leftField.setAccessible(true);
      Field rightField = clazz.getDeclaredField("right");
      rightField.setAccessible(true);

      int val = valField.getInt(node);
      Object left = leftField.get(node);
      Object right = rightField.get(node);

      return "TreeNode{val=" + val + ", left=" + treeNodeToString(left) + ", right="
          + treeNodeToString(right) + "}";
    } catch (Exception e) {
      return node.toString(); // fallback
    }
  }
}
