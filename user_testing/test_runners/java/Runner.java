package user_testing.test_runners.java;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.type.TypeReference;
import java.lang.reflect.Array;
import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Queue;
import java.util.Set;

public class Runner {
  private static Method userMethod;
  private static final ObjectMapper mapper = new ObjectMapper();
  private static String fullPackageClassName;

  private enum ParseType {
    INT,
    LONG,
    BOOLEAN,
    FLOAT,
    STRING,
    ARRAY,
    LIST,
    IMMUTABLE_LIST,
    SET,
    MAP,
    LISTNODE,
    TREENODE
  }

  public static void main(String[] args) throws Exception {
    if (args.length != 7 || (!"True".equals(args[3]) && !"False".equals(args[3]))) {
      System.err.println(
        "Usage: java Runner" + 
        " <practiceFilePackage>" +
        " <infoFilePath>.json" +
        " <testFilePath>.json" + 
        " <debug>, where <debug> is True or False." +
        " <SolutionClassName>" + 
        " <SolutionMethodName>" +
        " <ParseTypes list string>"
      );
      System.err.println("Given args: " + Arrays.toString(args));
      System.exit(1);
    }

    boolean debug = "True".equals(args[3]);

    try {
      String[] parseTypesArg = mapper.readValue(
        args[6],
        new TypeReference<String[]>() {}
      );
      ParseType[] parseTypes = ParseType.values();
      if (parseTypesArg.length != parseTypes.length) {
        throw new IllegalStateException("Given parse types argument must match" + 
                                        " the Java ParseType Enum, but they have different lengths.");
      }
      for (int i = 0; i < parseTypesArg.length; i++) {
        if (!parseTypes[i].name().equals(parseTypesArg[i].toUpperCase())) {
          throw new IllegalStateException("Given parse types argument must match" + 
                                  " the Java ParseType Enum, but this fails for type" + i + ".");
        }
      }

      Map<String, Object> root = mapper.readValue(
        Files.readAllBytes(Paths.get(args[1])),
        new TypeReference<Map<String, Object>>() {}
      );
      String practiceFilePackage = args[0];
      String requiredClassName = args[4];
      String requiredMethodName = args[5];
      Runner.fullPackageClassName = practiceFilePackage + "." + requiredClassName;

      @SuppressWarnings("unchecked")
      List<Map<String, Object>> inputDefs = (List<Map<String, Object>>) root.get("input_types");

      Class<?>[] paramTypes = new Class<?>[inputDefs.size()];
      for (int i = 0; i < inputDefs.size(); i++) {
        paramTypes[i] = parseType(inputDefs.get(i));
      }

      try {
        Class<?> clazz = Class.forName(fullPackageClassName);
        userMethod = clazz.getDeclaredMethod(requiredMethodName, paramTypes);
      } catch (NoSuchMethodException e) {
        printErr("Error: Practice file must contain" + " public " + requiredClassName
            + " class with appropriate public static " + requiredMethodName + " method.");
      }

      if (!Modifier.isStatic(userMethod.getModifiers())) {
        printErr("solve must be static.");
      }

      boolean unique = (boolean) root.get("unique_answer");
      @SuppressWarnings("unchecked")
      Map<String, Object> expectedType = (Map<String, Object>) root.get("expected_type_wrapper");
      
      List<Map<String, Object>> tests = mapper.readValue(
          Files.readAllBytes(Paths.get(args[2])),
          new TypeReference<List<Map<String, Object>>>() {}
      );
      
      for (int i = 0; i < tests.size(); i++) {
        Map<String, Object> test = tests.get(i);
        
        List<?> rawInputs = (List<?>) test.get("inputs");
        Object[] argsParsed = parseInputs(rawInputs, inputDefs);
        
        Object actual = userMethod.invoke(null, argsParsed);
        
        boolean fail = false;
        
        if (unique) {
          Object expected = parseValue(test.get("expected"), expectedType);
          if (!deepEquals(actual, expected))
            fail = true;
        } else {
          List<?> expectedList = (List<?>) test.get("expected");
          boolean ok = false;
          
          for (Object exp : expectedList) {
            Object parsed = parseValue(exp, expectedType);
            if (deepEquals(actual, parsed)) {
              ok = true;
              break;
            }
          }
          if (!ok)
            fail = true;
        }
        
        if (!validateType(actual, expectedType)) {
          printErr("Return type mismatch with expected_type");
        }
        
        if (fail) {
          printErr("Test " + (i + 1) + " failed. Incorrect value: " + deepToString(actual) + ".");
        }
      }
    } catch (Exception e) {
      if (!debug) {
        printErr(e.toString());
      } else {
        e.printStackTrace();
        System.exit(1);
      }
    }
      
    System.out.println("All tests passed");
  }

  // ===== TYPE PARSER =====

  private static void printErr(String msg) {
    System.err.println(msg);
    System.exit(1);
  }

  private static boolean isParseType(String candidate) {
    try {
      toParseType(candidate);
      return true;
    }  catch (IllegalArgumentException e) {
      return false;
    }
  }

  private static ParseType toParseType(String candidate) {
    return ParseType.valueOf(candidate.toUpperCase());
  }

  private static Class<?> parseType(Map<String, Object> def) {
    String candidate = (String) def.get("type");
    if (!isParseType(candidate)) {
      throw new IllegalArgumentException("Type fields should always refer to a ParseType," + 
                                         " untrue for " + candidate);
    }
    ParseType type = toParseType(candidate);
    return switch (type) {
      case INT -> int.class;
      case LONG -> long.class;
      case FLOAT -> double.class;
      case BOOLEAN -> boolean.class;
      case STRING -> String.class;
      case ARRAY -> {
        @SuppressWarnings("unchecked")
        Class<?> inner = parseType((Map<String, Object>) def.get("items"));
        yield Array.newInstance(inner, 0).getClass();
      }
      case LIST -> List.class;
      case IMMUTABLE_LIST -> {
        @SuppressWarnings("unchecked")
        Class<?> inner = parseType((Map<String, Object>) def.get("items"));
        yield Array.newInstance(inner, 0).getClass();
      }
      case SET -> Set.class;
      case MAP -> Map.class;
      case LISTNODE -> {
        try {
          yield Class.forName(fullPackageClassName + "$" + candidate);
        } catch (Exception e) {
          throw new RuntimeException("Missing class: " + candidate);
        }
      }
      case TREENODE -> {
        try {
          yield Class.forName(fullPackageClassName + "$" + candidate);
        } catch (Exception e) {
          throw new RuntimeException("Missing class: " + candidate);
        }
      }
    };
  }

  // ===== INPUT PARSING =====

  private static Object[] parseInputs(List<?> raw, List<Map<String, Object>> defs)
      throws Exception {
    if (raw.size() != defs.size()) {
      throw new RuntimeException("Input length mismatch");
    }

    Object[] res = new Object[raw.size()];
    for (int i = 0; i < raw.size(); i++) {
      res[i] = parseValue(raw.get(i), defs.get(i));
    }
    return res;
  }

  private static String getStringParseErrorMessage(String type) {
    return "Failed to parse what should be a " + type + " from a String.";
  }

  private static Object parseValue(Object val, Map<String, Object> def) throws Exception {
    String type = (String) def.get("type");
    if (val instanceof String) {
      String valStr = (String) val;
      switch (type) {
        case "int":
          try {
            return Integer.parseInt(valStr);
          } catch (NumberFormatException e) {
            System.err.println(getStringParseErrorMessage(type));
            throw e;
          }
        case "long":
          try {
            return Long.parseLong(valStr);
          } catch (NumberFormatException e) {
            System.err.println(getStringParseErrorMessage(type));
            throw e;
          }
        case "float":
          try {
            Double ret = Double.parseDouble(valStr);
            if (ret == 0)
              return 0.0; // handles -0.0
            return ret;
          } catch (NumberFormatException e) {
            System.err.println(getStringParseErrorMessage(type));
            throw e;
          }
        case "boolean":
          if (!valStr.equals("true") && !valStr.equals("false")) {
            System.err.println(getStringParseErrorMessage(type));
            throw new RuntimeException("Invalid boolean: " + valStr);
          }
          return Boolean.parseBoolean(valStr);
        case "string":
          return valStr;
        default:
          val = mapper.readValue(valStr, Object.class);
      }
    }
    switch (type) {
      case "int":
        return ((Number) val).intValue();
      case "long":
        return ((Number) val).longValue();
      case "float":
        return ((Number) val).doubleValue() == 0 ? 0.0 : ((Number) val).doubleValue();
      case "boolean":
        return val;
      case "string":
        return val;
      
      case "immutable_list":
      case "array": {
        // val must be a List after parsing
        List<?> rawList = (List<?>) val;
        @SuppressWarnings("unchecked")
        Map<String, Object> itemDef = (Map<String, Object>) def.get("items");
        Class<?> componentType = parseType(itemDef);
        Object array = Array.newInstance(componentType, rawList.size());

        for (int i = 0; i < rawList.size(); i++) {
          Array.set(array, i, parseValue(rawList.get(i), itemDef));
        }
        return array;
      }

      case "list": {
        List<?> raw = (List<?>) val;
        List<Object> list = new ArrayList<>();
        @SuppressWarnings("unchecked")
        Map<String, Object> inner = (Map<String, Object>) def.get("items");
        for (Object o : raw)
          list.add(parseValue(o, inner));
        return list;
      }

      case "set": {
        List<?> raw = (List<?>) val;
        Set<Object> set = new HashSet<>();
        @SuppressWarnings("unchecked")
        Map<String, Object> inner = (Map<String, Object>) def.get("items");
        for (Object o : raw)
          set.add(parseValue(o, inner));
        return set;
      }

      case "map": {
        Map<?, ?> raw = (Map<?, ?>) val;
        Map<Object, Object> map = new HashMap<>();
        @SuppressWarnings("unchecked")
        Map<String, Object> keyDef = (Map<String, Object>) def.get("keys");
        @SuppressWarnings("unchecked")
        Map<String, Object> valDef = (Map<String, Object>) def.get("values");

        for (Object k : raw.keySet()) {
          map.put(parseValue(k, keyDef), parseValue(raw.get(k), valDef));
        }
        return map;
      }

      case "ListNode":
        @SuppressWarnings("unchecked")
        Map<String, Object> def_val = (Map<String, Object>) def.get("val");
        return buildListNode((List<?>) val, def_val);

      case "TreeNode":
        @SuppressWarnings("unchecked")
        Map<String, Object> def_val2 = (Map<String, Object>) def.get("val");
        return buildTreeNode((List<?>) val, def_val2);

      default:
        throw new RuntimeException("Unknown type: " + type);
    }
  }

  // ===== TYPE VALIDATION =====

  private static boolean validateType(Object obj, Map<String, Object> def) {
    if (obj == null)
      return true;

    String type = (String) def.get("type");

    switch (type) {
      case "int":
        return obj instanceof Integer;
      case "long":
        return obj instanceof Long;
      case "float":
        return obj instanceof Double;
      case "boolean":
        return obj instanceof Boolean;
      case "string":
        return obj instanceof String;

      case "immutable_list":
      case "array":
        if (!obj.getClass().isArray())
          return false;
        int len = Array.getLength(obj);
        @SuppressWarnings("unchecked")
        Map<String, Object> inner = (Map<String, Object>) def.get("items");
        for (int i = 0; i < len; i++) {
          if (!validateType(Array.get(obj, i), inner))
            return false;
        }
        return true;

      case "list":
        if (!(obj instanceof List))
          return false;
        @SuppressWarnings("unchecked")
        Map<String, Object> listInner = (Map<String, Object>) def.get("items");
        for (Object o : (List<?>) obj) {
          if (!validateType(o, listInner))
            return false;
        }
        return true;

      case "set":
        if (!(obj instanceof Set))
          return false;
        @SuppressWarnings("unchecked")
        Map<String, Object> setInner = (Map<String, Object>) def.get("items");
        for (Object o : (Set<?>) obj) {
          if (!validateType(o, setInner))
            return false;
        }
        return true;

      case "map":
        if (!(obj instanceof Map))
          return false;
        @SuppressWarnings("unchecked")
        Map<String, Object> keyDef = (Map<String, Object>) def.get("keys");
        @SuppressWarnings("unchecked")
        Map<String, Object> valDef = (Map<String, Object>) def.get("values");

        for (Map.Entry<?, ?> e : ((Map<?, ?>) obj).entrySet()) {
          if (!validateType(e.getKey(), keyDef))
            return false;
          if (!validateType(e.getValue(), valDef))
            return false;
        }
        return true;

      case "ListNode":
      case "TreeNode":
        return obj.getClass().getName().equals(fullPackageClassName + "$" + type);

      default:
        throw new RuntimeException("Unknown type in validation: " + type);
    }
  }

  // ===== BUILDERS =====

  /**
   * Builds a ListNode from a list of raw values and the definition of its value type.
   *
   * @param vals    the list of values (already parsed as JSON objects)
   * @param valDef  the type definition for the ListNode's "val" field
   * @return the head ListNode, or null if the list is empty
   */
  private static Object buildListNode(List<?> vals, Map<String, Object> valDef) throws Exception {
    if (vals.isEmpty())
      return null;

    Class<?> clazz = Class.forName(fullPackageClassName + "$ListNode");
    Class<?> valType = parseType(valDef);
    Constructor<?> ctor = clazz.getConstructor(valType, clazz);

    // Build the head node
    Object headVal = parseValue(vals.get(0), valDef);
    Object head = ctor.newInstance(headVal, null);

    // Link the rest
    Object prev = head;
    Field nextField = clazz.getDeclaredField("next");
    nextField.setAccessible(true);

    for (int i = 1; i < vals.size(); i++) {
      Object currVal = parseValue(vals.get(i), valDef);
      Object curr = ctor.newInstance(currVal, null);
      nextField.set(prev, curr);
      prev = curr;
    }

    return head;
  }

  /**
   * Builds a TreeNode from a list of level‑order values and the definition of its value type.
   *
   * @param vals    the level‑order list (may contain nulls for missing nodes)
   * @param valDef  the type definition for the TreeNode's "val" field
   * @return the root TreeNode, or null if the list is empty
   */
  private static Object buildTreeNode(List<?> vals, Map<String, Object> valDef) throws Exception {
    if (vals.isEmpty())
      return null;

    Class<?> clazz = Class.forName(fullPackageClassName + "$TreeNode");
    Class<?> valType = parseType(valDef);
    Constructor<?> ctor = clazz.getConstructor(valType, clazz, clazz);

    // Parse the root value (first element) – it must not be null
    Object rootVal = parseValue(vals.get(0), valDef);
    Object root = ctor.newInstance(rootVal, null, null);

    Queue<Object> queue = new LinkedList<>();
    queue.add(root);

    Field leftField = clazz.getDeclaredField("left");
    Field rightField = clazz.getDeclaredField("right");
    leftField.setAccessible(true);
    rightField.setAccessible(true);

    int i = 1;
    while (!queue.isEmpty() && i < vals.size()) {
      Object node = queue.poll();

      // Left child
      if (vals.get(i) != null) {
        Object leftVal = parseValue(vals.get(i), valDef);
        Object leftNode = ctor.newInstance(leftVal, null, null);
        leftField.set(node, leftNode);
        queue.add(leftNode);
      }
      i++;

      // Right child
      if (i < vals.size() && vals.get(i) != null) {
        Object rightVal = parseValue(vals.get(i), valDef);
        Object rightNode = ctor.newInstance(rightVal, null, null);
        rightField.set(node, rightNode);
        queue.add(rightNode);
      }
      i++;
    }

    return root;
  }

  // ===== DEEP EQUALS =====

  private static boolean isListNode(Object o) {
    return o != null && o.getClass().getName().endsWith("$ListNode");
  }

  private static boolean isTreeNode(Object o) {
    return o != null && o.getClass().getName().endsWith("$TreeNode");
  }

  private static boolean deepEquals(Object a, Object b) {
    if (a == b)
      return true;
    if (a == null || b == null)
      return false;

    if (a.getClass().isArray() && b.getClass().isArray()) {
      Object[] ba = (Object[]) box(a);
      Object[] bb = (Object[]) box(b);
      if (ba.length != bb.length) return false;
      for (int i = 0; i < ba.length; i++) {
        if (!deepEquals(ba[i], bb[i])) return false;
      }
      return true;
    }

    if (a instanceof Set && b instanceof Set) {
      Set<?> s1 = (Set<?>) a, s2 = (Set<?>) b;
      if (s1.size() != s2.size())
        return false;

      outer: for (Object x : s1) {
        for (Object y : s2) {
          if (deepEquals(x, y))
            continue outer;
        }
        return false;
      }
      return true;
    }

    if (a instanceof Collection && b instanceof Collection) {
      Iterator<?> i1 = ((Collection<?>) a).iterator();
      Iterator<?> i2 = ((Collection<?>) b).iterator();
      while (i1.hasNext()) {
        if (!i2.hasNext() || !deepEquals(i1.next(), i2.next()))
          return false;
      }
      return !i2.hasNext();
    }

    if (a instanceof Map && b instanceof Map) {
      Map<?, ?> m1 = (Map<?, ?>) a;
      Map<?, ?> m2 = (Map<?, ?>) b;
      if (m1.size() != m2.size())
        return false;

      outer: for (Object k1 : m1.keySet()) {
        for (Object k2 : m2.keySet()) {
          if (deepEquals(k1, k2)) {
            if (!deepEquals(m1.get(k1), m2.get(k2)))
              return false;
            continue outer;
          }
        }
        return false;
      }
      return true;
    }

    if (isListNode(a) && isListNode(b)) {
      return compareListNode(a, b, new HashSet<>());
    }

    if (isTreeNode(a) && isTreeNode(b)) {
      return compareTreeNode(a, b, new HashSet<>());
    }

    return a.equals(b);
  }

  private static boolean compareListNode(Object a, Object b, Set<String> visited) {
    if (a == b)
      return true;
    if (a == null || b == null)
      return false;

    String key = System.identityHashCode(a) + ":" + System.identityHashCode(b);
    if (visited.contains(key))
      return true;
    visited.add(key);

    try {
      Class<?> clazz = a.getClass();

      Field val = clazz.getDeclaredField("val");
      Field next = clazz.getDeclaredField("next");
      val.setAccessible(true);
      next.setAccessible(true);

      Object v1 = val.get(a);
      Object v2 = val.get(b);

      if (!deepEquals(v1, v2))
        return false;

      Object n1 = next.get(a);
      Object n2 = next.get(b);

      return compareListNode(n1, n2, visited);

    } catch (Exception e) {
      throw new RuntimeException(e);
    }
  }

  private static boolean compareTreeNode(Object a, Object b, Set<String> visited) {
    if (a == b)
      return true;
    if (a == null || b == null)
      return false;

    String key = System.identityHashCode(a) + ":" + System.identityHashCode(b);
    if (visited.contains(key))
      return true;
    visited.add(key);

    try {
      Class<?> clazz = a.getClass();

      Field val = clazz.getDeclaredField("val");
      Field left = clazz.getDeclaredField("left");
      Field right = clazz.getDeclaredField("right");

      val.setAccessible(true);
      left.setAccessible(true);
      right.setAccessible(true);

      Object v1 = val.get(a);
      Object v2 = val.get(b);

      if (!deepEquals(v1, v2))
        return false;

      Object l1 = left.get(a);
      Object l2 = left.get(b);

      Object r1 = right.get(a);
      Object r2 = right.get(b);

      return compareTreeNode(l1, l2, visited) && compareTreeNode(r1, r2, visited);

    } catch (Exception e) {
      throw new RuntimeException(e);
    }
  }

  private static Object box(Object arr) {
    if (arr instanceof int[]) {
      int[] a = (int[]) arr;
      Integer[] b = new Integer[a.length];
      for (int i = 0; i < a.length; i++)
        b[i] = a[i];
      return b;
    }
    if (arr instanceof long[]) {
      long[] a = (long[]) arr;
      Long[] b = new Long[a.length];
      for (int i = 0; i < a.length; i++)
        b[i] = a[i];
      return b;
    }
    if (arr instanceof double[]) {
      double[] a = (double[]) arr;
      Double[] b = new Double[a.length];
      for (int i = 0; i < a.length; i++)
        b[i] = a[i];
      return b;
    }
    if (arr instanceof boolean[]) {
      boolean[] a = (boolean[]) arr;
      Boolean[] b = new Boolean[a.length];
      for (int i = 0; i < a.length; i++)
        b[i] = a[i];
      return b;
    }
    return arr;
  }

  private static String deepToString(Object o) {
    if (o == null)
      return "null";
    if (o.getClass().isArray())
      return Arrays.deepToString((Object[]) box(o));
    return o.toString();
  }
}