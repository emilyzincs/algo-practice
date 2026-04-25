package user_testing.test_runners.java;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.type.TypeReference;
import java.lang.reflect.Array;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.Comparator;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Set;


// Main test runner for Java solutions. Reads test definitions, invokes the user's method,
// and compares results using deep equality.
public class Runner {
  private static final ObjectMapper mapper = new ObjectMapper();
  private static final AgnosticComparator AGNOSTIC_COMPARATOR = new AgnosticComparator();
  private static String fullPackageClassName;

  // Enumeration of all supported data types for parsing and validation.
  private enum ParseType {
    INT,
    LONG,
    BOOLEAN,
    FLOAT,
    STRING,
    ARRAY,
    LIST,
    UNORDERED_LIST,
  }

  // Entry point: validates arguments, loads the user's class, runs all tests,
  // and prints the result.
  //
  // Parameters:
  // - args[0]: practiceFilePackage – package name of the user's solution.
  // - args[1]: infoFilePath – JSON file describing input/output types.
  // - args[2]: testFilePath – JSON file containing the test cases.
  // - args[3]: debug – "True" or "False", enables stack trace on error.
  // - args[4]: SolutionClassName – name of the class containing the method.
  // - args[5]: SolutionMethodName – name of the method to test.
  // - args[6]: ParseTypes list string – JSON array of strings matching ParseType enum.
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

      Class<?> clazz = null;
      Method userMethod = null;
      try {
        clazz = Class.forName(fullPackageClassName);
        userMethod = clazz.getDeclaredMethod(requiredMethodName, paramTypes);
        int mod = userMethod.getModifiers();
        if (!Modifier.isPublic(mod)) {
          printErr("Error: Method '" + requiredMethodName + "' must be public.");
        } else if (Modifier.isStatic(mod)) {
          printErr("Error: Method '" + requiredMethodName + "' must not be static.");
        } else if (Modifier.isAbstract(mod)) {
          printErr("Error: Method '" + requiredMethodName + "' must be concrete (not abstract).");
        }
      } catch (NoSuchMethodException e) {
          printErr("Error: Practice file must contain a public class '" + requiredClassName 
                  + "' with a public instance method '" + requiredMethodName 
                  + "' matching the expected parameter types.");
      }
      
      boolean unique = (boolean) root.get("unique_answer");
      @SuppressWarnings("unchecked")
      Map<String, Object> expectedType = (Map<String, Object>) root.get("expected_type");
      
      List<Map<String, Object>> tests = mapper.readValue(
          Files.readAllBytes(Paths.get(args[2])),
          new TypeReference<List<Map<String, Object>>>() {}
      );
      
      for (int i = 0; i < tests.size(); i++) {
        Object instance = null;
        try {
          instance = clazz.getDeclaredConstructor().newInstance();
        } catch (NoSuchMethodException e) {
          printErr("Error: Class '" + requiredClassName + "' must have a public no‑argument constructor.");
        } catch (Exception e) {
          printErr("Error: Could not instantiate class '" + requiredClassName + "': " + e.getMessage());
        }

        Map<String, Object> test = tests.get(i);
        
        List<?> rawInputs = (List<?>) test.get("inputs");
        Object[] argsParsed = parseInputs(rawInputs, inputDefs);
        
        Object raw = userMethod.invoke(instance, argsParsed);
        Object actual = standardizeOutput(raw, expectedType);
        
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
        
        if (fail) {
          printErr("Test " + (i + 1) + " failed.");
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

  // Prints the given error message and terminates the program with exit code 1.
  private static void printErr(String msg) {
    System.err.println(msg);
    System.exit(1);
  }

  // Converts the 'candidate' string to a ParseType enum constant (case‑insensitive),
  // returning the corresponding ParseType value on success, and throwing an
  // IllegalArgumentException on failure.
  private static ParseType toParseType(String candidate) {
    try {
      return ParseType.valueOf(candidate.toUpperCase());
    } catch (IllegalArgumentException e) {
      throw new IllegalArgumentException("Type fields should always refer to a ParseType," + 
                                         " untrue for " + candidate);
    }
  }

  // Converts a type definition (JSON map) into the corresponding Java Class object.
  //
  // Parameters:
  // - def: A map containing at least a "type" key; for container types also "items", "keys", "values".
  //
  // Returns:
  //   The Java Class representing that type (e.g., int.class, List.class).
  private static Class<?> parseType(Map<String, Object> def) {
    String candidate = (String) def.get("type");
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
      case LIST, UNORDERED_LIST -> List.class;
    };
  }

  // Parses a list of raw inputs into an array of Java objects according to the given definitions.
  //
  // Parameters:
  // - raw: List of raw JSON values (already partially parsed).
  // - defs: List of type definitions, one per input.
  //
  // Returns:
  //   An Object[] suitable for passing to the user's method via reflection.
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

  // Parses a single value from JSON according to a type definition.
  //
  // Parameters:
  // - val: The raw JSON value (may be a String, Number, List, Map, etc.).
  // - def: The type definition map.
  //
  // Returns:
  //   The parsed Java object (Integer, Long, Double, Boolean, String, array, List, Set, Map).
  private static Object parseValue(Object val, Map<String, Object> def) throws Exception {
    String candidate = (String) def.get("type");
    ParseType type = toParseType(candidate);

    return switch (type) {
      case INT -> ((Number) val).intValue();
      case LONG -> ((Number) val).longValue();
      case FLOAT -> ((Number) val).doubleValue() == 0 ? 0.0 : ((Number) val).doubleValue();
      case BOOLEAN, STRING -> val;
      case ARRAY -> {
        List<?> rawList = (List<?>) val;
        @SuppressWarnings("unchecked")
        Map<String, Object> itemDef = (Map<String, Object>) def.get("items");
        Class<?> componentType = parseType(itemDef);
        Object array = Array.newInstance(componentType, rawList.size());

        for (int i = 0; i < rawList.size(); i++) {
          Array.set(array, i, parseValue(rawList.get(i), itemDef));
        }
        yield array;
      }
      case LIST, UNORDERED_LIST -> {
        List<?> raw = (List<?>) val;
        List<Object> list = new ArrayList<>();
        @SuppressWarnings("unchecked")
        Map<String, Object> inner = (Map<String, Object>) def.get("items");
        for (Object o : raw) {
          list.add(parseValue(o, inner));
        }
        yield list;
      }
    };
  }

  private static Object standardizeOutput(Object val, Map<String, Object> def) throws Exception {
    String candidate = (String) def.get("type");
    ParseType type = toParseType(candidate);

    return switch (type) {
      case INT -> {
        typeAssert(val, Integer.class, type);
        yield ((Number) val).intValue();
      }
      case LONG -> {
        typeAssert(val, Long.class, type);
        yield ((Number) val).longValue();
      }
      case FLOAT -> {
        typeAssert(val, Number.class, type); // Checks if it's any numeric type
        double d = ((Number) val).doubleValue();
        yield d == 0 ? 0.0 : d;
      }
      case BOOLEAN -> {
        typeAssert(val, Boolean.class, type);
        yield val;
      }
      case STRING -> {
        typeAssert(val, String.class, type);
        yield val;
      }
      case ARRAY -> {
        if (val == null || !val.getClass().isArray()) {
          throw new IllegalArgumentException("Expected List or Array for type ARRAY");
        }
        List<?> rawList = Arrays.asList((Object[]) box(val));
        @SuppressWarnings("unchecked")
        Map<String, Object> itemDef = (Map<String, Object>) def.get("items");
        Class<?> componentType = parseType(itemDef);
        Object array = Array.newInstance(componentType, rawList.size());
        for (int i = 0; i < rawList.size(); i++) {
          Array.set(array, i, standardizeOutput(rawList.get(i), itemDef));
        }
        yield array;
      }
      case LIST, UNORDERED_LIST -> {
        typeAssert(val, List.class, type);
        List<?> raw = (List<?>) val;
        List<Object> list = new ArrayList<>();
        @SuppressWarnings("unchecked")
        Map<String, Object> inner = (Map<String, Object>) def.get("items");
        for (Object o : raw) {
          list.add(standardizeOutput(o, inner));
        }
        if (type == ParseType.UNORDERED_LIST) {
          Collections.sort(list, AGNOSTIC_COMPARATOR);
        }
        yield list;
      }
    };
  }

  private static void typeAssert(Object val, Class<?> expected, ParseType type) {
    if (!expected.isInstance(val)) {
      throw new IllegalArgumentException(
        String.format("Expected %s for type %s, but got %s", 
          expected.getSimpleName(), 
          type, 
          (val == null ? "null" : val.getClass().getSimpleName()))
      );
    }
  }

  // Performs a deep equality comparison between two objects.
  // Returns true if the objects are deeply equal, false otherwise.
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

    return a.equals(b);
  }

  // Converts a primitive array into an array of its boxed wrapper type.
  // Non‑primitive arrays are returned unchanged.
  //
  // Parameters:
  // - arr: The array (may be primitive or object array).
  //
  // Returns:
  //   An Object[] of boxed values (or the original array if already boxed).
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

  public static class AgnosticComparator implements Comparator<Object> {
    @Override
    public int compare(Object a, Object b) {
      if (a.getClass() != b.getClass()) {
        throw new IllegalArgumentException(
          "Type Mismatch: Cannot compare " + a.getClass().getSimpleName() + 
          " and " + b.getClass().getSimpleName()
        );
      }

      if (a instanceof String) {
        return ((String) a).compareTo((String) b);
      }
      if (a instanceof Number) {
        return Double.compare(((Number) a).doubleValue(), ((Number) b).doubleValue());
      }
      if (a instanceof Boolean) {
        return Boolean.compare((Boolean) a, (Boolean) b);
      }
      if (a instanceof List) {
        List<?> listA = (List<?>) a;
        List<?> listB = (List<?>) b;
        
        int minSize = Math.min(listA.size(), listB.size());
        for (int i = 0; i < minSize; i++) {
          int cmp = compare(listA.get(i), listB.get(i));
          if (cmp != 0) return cmp;
        }
        return Integer.compare(listA.size(), listB.size());
      }
      if (a.getClass().isArray()) {
        Object[] arrA = (Object[]) a;
        Object[] arrB = (Object[]) b;
        
        int minSize = Math.min(arrA.length, arrB.length);
        for (int i = 0; i < minSize; i++) {
          int cmp = compare(arrA[i], arrB[i]);
          if (cmp != 0) return cmp;
        }
        return Integer.compare(arrA.length, arrB.length);
      }

      throw new UnsupportedOperationException("Unknown type: " + a.getClass());
    }
  }
}
