# General Implementation Requirements
- The implementation must be fully self-contained inside the practice file (whose path is printed upon starting practice of an algorithm).
- The practice file must have a top-level (i.e., non-nested) ```Solution``` class containing a ```solve``` method which attempts to implement the current algorithm. For language-specifics clarifications, see [Language-Level Requirements](#language-level-requirements).
- If there are classes in the expected ```solve``` method declaration that are not built into the language (e.g. ListNode), those classes must be fully implemented in the practice file and match the expected implementation. Going forward, we refer to such classes as Required Classes. For more details, see [Required Classes](#required-classes).

## Language-Level Requirements

### Python
- Required Classes must be written in the top-level of the practice file.

### Java

When qualifiers are described below, it means *exactly* those qualifiers and no more.
- The ```Solution``` class must be public, and the ```solve``` method must just be public and static.
- Required Classes must be written inside the ```Solution``` class. They must be public and static, and their required constructor must be public.

## Required Classes
Recall that Required Classes are classes in the expected ```solve``` method declaration that are not built into the language. The possible Required Classes are listed below, along with details about the fields.
When implemented, the details must exactly match. 

Required classes must also include at least one callable constructor that takes in and initializes all fields in the order they are listed below. For example, a python ListNode implementation must include a constructor ```__init__(self, val, next):``` that sets self.val to val and self.next to next.

[Language-Level Requirements](#language-level-requirements) includes language-level clarifications about Required Classes.

### ListNode
  
| Field Name | Type                                                               |
|------------|----------------------------------------------------------------    |
| val        | Determined by the algorithm's expected input types/return type     |
| next       | ListNode (nullable)                                                |            

### TreeNode

| Field Name | Type                                                               |
|------------|----------------------------------------------------------------    |
| val        | Determined by the algorithm's expected input types/return type     |
| left       | TreeNode (nullable)                                                | 
| right      | TreeNode (nullable)                                                |       
