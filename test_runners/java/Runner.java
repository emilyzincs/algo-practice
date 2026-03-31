package test_runners.java;

import com.fasterxml.jackson.databind.ObjectMapper;
import java.lang.reflect.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;

public class Runner {
  private static Method userMethod;
  private static final ObjectMapper mapper = new ObjectMapper();

  public static void main(String[] args) throws Exception {
    if (args.length != 4) {
      System.err.println("Usage: java Runner <alg>" +
                        " <testFileName>.json> <SolutionClassName> <SolutionMethodName>");
      System.exit(1);
    }

    Map<String, Object> root = mapper.readValue(
        Files.readAllBytes(Paths.get(args[1])), Map.class);
    
    String requiredClassName = args[2];
    String requiredMethodName = args[3];

    List<Map<String, Object>> inputDefs =
        (List<Map<String, Object>>) root.get("input_types");

    Class<?>[] paramTypes = new Class<?>[inputDefs.size()];
    for (int i = 0; i < inputDefs.size(); i++) {
      paramTypes[i] = parseType(inputDefs.get(i));
    }

    try {
      Class<?> clazz = Class.forName("practice." + requiredClassName);
      userMethod = clazz.getDeclaredMethod(requiredMethodName, paramTypes);
    } catch (NoSuchMethodException e) {
      System.err.println("Error: Practice file must contain" + 
                          " public 'Solution' class with appropriate public static 'solve' method.");
      System.exit(1);
    }

    if (!Modifier.isStatic(userMethod.getModifiers())) {
      throw new RuntimeException("solve must be static");
    }

    boolean unique = (boolean) root.get("unique_answer");
    Map<String, Object> expectedType =
        (Map<String, Object>) root.get("expected_type_wrapper");

    List<Map<String, Object>> tests =
        (List<Map<String, Object>>) root.get("tests");

    for (int i = 0; i < tests.size(); i++) {
      Map<String, Object> test = tests.get(i);

      List<?> rawInputs = (List<?>) test.get("inputs");
      Object[] argsParsed = parseInputs(rawInputs, inputDefs);

      Object actual = userMethod.invoke(null, argsParsed);

      boolean fail = false;

      if (unique) {
        Object expected = parseValue(test.get("expected"), expectedType);
        if (!deepEquals(actual, expected)) fail = true;
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
        if (!ok) fail = true;
      }

      if (!validateType(actual, expectedType)) {
        throw new RuntimeException("Return type mismatch with expected_type");
      }

      if (fail) {
        System.err.println("Test " + (i + 1) + " failed. Incorrect value: "
            + deepToString(actual) + ".");
        System.exit(1);
      }
    }

    System.out.println("All tests passed");
  }

  // ===== TYPE PARSER =====

  private static Class<?> parseType(Map<String, Object> def) {
    String type = (String) def.get("type");

    switch (type) {
      case "int": return int.class;
      case "long": return long.class;
      case "float": return double.class;
      case "boolean": return boolean.class;
      case "string": return String.class;

      case "array": {
        Class<?> inner = parseType((Map<String, Object>) def.get("items"));
        return Array.newInstance(inner, 0).getClass();
      }

      case "list": return List.class;
      case "set": return Set.class;
      case "map": return Map.class;

      case "ListNode":
      case "TreeNode":
        try {
          return Class.forName("practice." + type);
        } catch (Exception e) {
          throw new RuntimeException("Missing class: " + type);
        }

      default:
        throw new RuntimeException("Unknown type: " + type);
    }
  }

  // ===== INPUT PARSING =====

  private static Object[] parseInputs(List<?> raw, List<Map<String, Object>> defs) throws Exception {
    if (raw.size() != defs.size()) {
      throw new RuntimeException("Input length mismatch");
    }

    Object[] res = new Object[raw.size()];
    for (int i = 0; i < raw.size(); i++) {
      res[i] = parseValue(raw.get(i), defs.get(i));
    }
    return res;
  }

  private static Object parseValue(Object val, Map<String, Object> def) throws Exception {
    String type = (String) def.get("type");

    switch (type) {
      case "int": return ((Number) val).intValue();
      case "long": return ((Number) val).longValue();
      case "float": return ((Number) val).doubleValue();
      case "boolean": return val;
      case "string": return val;

      case "array":
        return mapper.convertValue(val, parseType(def));

      case "list": {
        List<?> raw = (List<?>) val;
        List<Object> list = new ArrayList<>();
        Map<String, Object> inner = (Map<String, Object>) def.get("items");
        for (Object o : raw) list.add(parseValue(o, inner));
        return list;
      }

      case "set": {
        List<?> raw = (List<?>) val;
        Set<Object> set = new HashSet<>();
        Map<String, Object> inner = (Map<String, Object>) def.get("items");
        for (Object o : raw) set.add(parseValue(o, inner));
        return set;
      }

      case "map": {
        Map<?, ?> raw = (Map<?, ?>) val;
        Map<Object, Object> map = new HashMap<>();

        Map<String, Object> keyDef = (Map<String, Object>) def.get("keys");
        Map<String, Object> valDef = (Map<String, Object>) def.get("values");

        for (Object k : raw.keySet()) {
          map.put(parseValue(k, keyDef),
                  parseValue(raw.get(k), valDef));
        }
        return map;
      }

      case "ListNode":
        return buildListNode((List<?>) val);

      case "TreeNode":
        return buildTreeNode((List<?>) val);

      default:
        throw new RuntimeException("Unknown type: " + type);
    }
  }

  // ===== TYPE VALIDATION (NEW) =====

  private static boolean validateType(Object obj, Map<String, Object> def) {
    if (obj == null) return true;

    String type = (String) def.get("type");

    switch (type) {
      case "int": return obj instanceof Integer;
      case "long": return obj instanceof Long;
      case "float": return obj instanceof Double;
      case "boolean": return obj instanceof Boolean;
      case "string": return obj instanceof String;

      case "array":
        if (!obj.getClass().isArray()) return false;
        int len = Array.getLength(obj);
        Map<String, Object> inner = (Map<String, Object>) def.get("items");
        for (int i = 0; i < len; i++) {
          if (!validateType(Array.get(obj, i), inner)) return false;
        }
        return true;

      case "list":
        if (!(obj instanceof List)) return false;
        Map<String, Object> listInner = (Map<String, Object>) def.get("items");
        for (Object o : (List<?>) obj) {
          if (!validateType(o, listInner)) return false;
        }
        return true;

      case "set":
        if (!(obj instanceof Set)) return false;
        Map<String, Object> setInner = (Map<String, Object>) def.get("items");
        for (Object o : (Set<?>) obj) {
          if (!validateType(o, setInner)) return false;
        }
        return true;

      case "map":
        if (!(obj instanceof Map)) return false;
        Map<String, Object> keyDef = (Map<String, Object>) def.get("keys");
        Map<String, Object> valDef = (Map<String, Object>) def.get("values");

        for (Map.Entry<?, ?> e : ((Map<?, ?>) obj).entrySet()) {
          if (!validateType(e.getKey(), keyDef)) return false;
          if (!validateType(e.getValue(), valDef)) return false;
        }
        return true;

      default:
        return true;
    }
  }

  // ===== BUILDERS =====

  private static Object buildListNode(List<?> vals) throws Exception {
    Class<?> clazz = Class.forName("practice.ListNode");
    Constructor<?> ctor = clazz.getConstructor(int.class);

    Object dummy = ctor.newInstance(0);
    Object cur = dummy;

    Field next = clazz.getDeclaredField("next");
    next.setAccessible(true);

    for (Object v : vals) {
      Object node = ctor.newInstance(((Number) v).intValue());
      next.set(cur, node);
      cur = node;
    }

    return next.get(dummy);
  }

  private static Object buildTreeNode(List<?> vals) throws Exception {
    if (vals.isEmpty()) return null;

    Class<?> clazz = Class.forName("practice.TreeNode");
    Constructor<?> ctor = clazz.getConstructor(int.class);

    Object root = ctor.newInstance(((Number) vals.get(0)).intValue());
    Queue<Object> q = new LinkedList<>();
    q.add(root);

    Field left = clazz.getDeclaredField("left");
    Field right = clazz.getDeclaredField("right");
    left.setAccessible(true);
    right.setAccessible(true);

    int i = 1;

    while (!q.isEmpty() && i < vals.size()) {
      Object node = q.poll();

      if (vals.get(i) != null) {
        Object l = ctor.newInstance(((Number) vals.get(i)).intValue());
        left.set(node, l);
        q.add(l);
      }
      i++;

      if (i < vals.size() && vals.get(i) != null) {
        Object r = ctor.newInstance(((Number) vals.get(i)).intValue());
        right.set(node, r);
        q.add(r);
      }
      i++;
    }

    return root;
  }

  // ===== DEEP EQUALS =====

  private static boolean deepEquals(Object a, Object b) {
    if (a == b) return true;
    if (a == null || b == null) return false;

    if (a.getClass().isArray() && b.getClass().isArray()) {
      return Arrays.deepEquals((Object[]) box(a), (Object[]) box(b));
    }

    if (a instanceof Set && b instanceof Set) {
      Set<?> s1 = (Set<?>) a, s2 = (Set<?>) b;
      if (s1.size() != s2.size()) return false;

      outer:
      for (Object x : s1) {
        for (Object y : s2) {
          if (deepEquals(x, y)) continue outer;
        }
        return false;
      }
      return true;
    }

    if (a instanceof Collection && b instanceof Collection) {
      Iterator<?> i1 = ((Collection<?>) a).iterator();
      Iterator<?> i2 = ((Collection<?>) b).iterator();
      while (i1.hasNext()) {
        if (!i2.hasNext() || !deepEquals(i1.next(), i2.next())) return false;
      }
      return !i2.hasNext();
    }

    if (a instanceof Map && b instanceof Map) {
      Map<?, ?> m1 = (Map<?, ?>) a;
      Map<?, ?> m2 = (Map<?, ?>) b;
      if (m1.size() != m2.size()) return false;

      for (Object k : m1.keySet()) {
        if (!m2.containsKey(k)) return false;
        if (!deepEquals(m1.get(k), m2.get(k))) return false;
      }
      return true;
    }

    return a.equals(b);
  }

  private static Object box(Object arr) {
    if (arr instanceof int[]) {
      int[] a = (int[]) arr;
      Integer[] b = new Integer[a.length];
      for (int i = 0; i < a.length; i++) b[i] = a[i];
      return b;
    }
    if (arr instanceof long[]) {
      long[] a = (long[]) arr;
      Long[] b = new Long[a.length];
      for (int i = 0; i < a.length; i++) b[i] = a[i];
      return b;
    }
    if (arr instanceof double[]) {
      double[] a = (double[]) arr;
      Double[] b = new Double[a.length];
      for (int i = 0; i < a.length; i++) b[i] = a[i];
      return b;
    }
    if (arr instanceof boolean[]) {
      boolean[] a = (boolean[]) arr;
      Boolean[] b = new Boolean[a.length];
      for (int i = 0; i < a.length; i++) b[i] = a[i];
      return b;
    }
    return arr;
  }

  private static String deepToString(Object o) {
    if (o == null) return "null";
    if (o.getClass().isArray()) return Arrays.deepToString((Object[]) box(o));
    return o.toString();
  }
}