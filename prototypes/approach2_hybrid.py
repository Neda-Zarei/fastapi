"""
Prototype Approach 2: Hybrid with Function-Specific Overrides

This approach extracts common parameters to a base signature using **kwargs,
while keeping function-specific parameters (convert_underscores, embed, media_type)
explicitly in the function signatures.

This balances DRY principles with clarity for function-specific behavior.

Testing functions: Path, Query, Header (shows different param combinations)
"""

from typing import Any, Callable, Dict, List, Optional, Union

from annotated_doc import Doc
from fastapi import params
from fastapi._compat import Undefined
from fastapi.openapi.models import Example
from typing_extensions import Annotated, deprecated

_Unset: Any = Undefined

# ============================================================================
# COMMON PARAMETER KWARGS DEFINITION
# ============================================================================

# Define a TypedDict-style documentation for common parameters
# This serves as documentation for what kwargs are accepted

COMMON_PARAM_DOCS = """
Common Parameters (accepted as **kwargs):
    
    default: Default value if the parameter field is not set.
    default_factory: A callable to generate the default value.
    alias: An alternative name for the parameter field.
    alias_priority: Priority of the alias. This affects whether an alias generator is used.
    validation_alias: 'Whitelist' validation step. The parameter field will be the single one
        allowed by the alias or set of aliases defined.
    serialization_alias: 'Blacklist' validation step. The vanilla parameter field will be the
        single one of the alias' or set of aliases' fields and all the other fields will be
        ignored at serialization time.
    title: Human-readable title.
    description: Human-readable description.
    gt: Greater than. If set, value must be greater than this. Only applicable to numbers.
    ge: Greater than or equal. If set, value must be greater than or equal to this. Only applicable to numbers.
    lt: Less than. If set, value must be less than this. Only applicable to numbers.
    le: Less than or equal. If set, value must be less than or equal to this. Only applicable to numbers.
    min_length: Minimum length for strings.
    max_length: Maximum length for strings.
    pattern: RegEx pattern for strings.
    regex: RegEx pattern for strings (deprecated, use pattern instead).
    discriminator: Parameter field name for discriminating the type in a tagged union.
    strict: If `True`, strict validation is applied to the field.
    multiple_of: Value must be a multiple of this. Only applicable to numbers.
    allow_inf_nan: Allow `inf`, `-inf`, `nan`. Only applicable to numbers.
    max_digits: Maximum number of allow digits for strings.
    decimal_places: Maximum number of decimal places allowed for numbers.
    examples: Example values for this field.
    example: Example value (deprecated, use examples instead).
    openapi_examples: OpenAPI-specific examples.
    deprecated: Mark this parameter field as deprecated.
    include_in_schema: To include (or not) this parameter field in the generated OpenAPI.
    json_schema_extra: Any additional JSON schema data.
"""


def _forward_common_params(**kwargs: Any) -> Dict[str, Any]:
    """
    Process and forward common parameters to params classes.
    
    This helper validates and normalizes common parameters while maintaining
    backward compatibility with all standard parameter options.
    """
    # Simply return the kwargs - actual validation happens in params.py
    return kwargs


# ============================================================================
# FUNCTION IMPLEMENTATIONS - Hybrid Approach
# ============================================================================


def Path(  # noqa: N802
    default: Annotated[
        Any,
        Doc(
            """
            Default value if the parameter field is not set.

            This doesn't affect `Path` parameters as the value is always required.
            The parameter is available only for compatibility.
            """
        ),
    ] = ...,
    **common_params: Any,
) -> Any:
    """
    Declare a path parameter for a *path operation*.

    Read more about it in the
    [FastAPI docs for Path Parameters and Numeric Validations](https://fastapi.tiangolo.com/tutorial/path-params-numeric-validations/).
    
    All standard validation and documentation parameters are supported via **common_params.
    See COMMON_PARAM_DOCS for full list of available parameters.

    ```python
    from typing import Annotated

    from fastapi import FastAPI, Path

    app = FastAPI()


    @app.get("/items/{item_id}")
    async def read_items(
        item_id: Annotated[int, Path(title="The ID of the item to get", gt=0)],
    ):
        return {"item_id": item_id}
    ```
    """
    processed_params = _forward_common_params(**common_params)
    return params.Path(default=default, **processed_params)


def Query(  # noqa: N802
    default: Annotated[
        Any,
        Doc(
            """
            Default value if the parameter field is not set.
            """
        ),
    ] = Undefined,
    **common_params: Any,
) -> Any:
    """
    Declare a query parameter for a *path operation*.
    
    All standard validation and documentation parameters are supported via **common_params.
    See COMMON_PARAM_DOCS for full list of available parameters.
    """
    processed_params = _forward_common_params(**common_params)
    return params.Query(default=default, **processed_params)


def Header(  # noqa: N802
    default: Annotated[
        Any,
        Doc(
            """
            Default value if the parameter field is not set.
            """
        ),
    ] = Undefined,
    *,
    convert_underscores: Annotated[
        bool,
        Doc(
            """
            Automatically convert underscores to hyphens in the parameter field name.

            Read more about it in the
            [FastAPI docs for Header Parameters](https://fastapi.tiangolo.com/tutorial/header-params/#automatic-conversion)
            """
        ),
    ] = True,
    **common_params: Any,
) -> Any:
    """
    Declare a header parameter for a *path operation*.
    
    The convert_underscores parameter is specific to headers and controls automatic
    conversion of Python underscore naming to HTTP header hyphen naming.
    
    All standard validation and documentation parameters are supported via **common_params.
    See COMMON_PARAM_DOCS for full list of available parameters.
    """
    processed_params = _forward_common_params(**common_params)
    return params.Header(
        default=default, convert_underscores=convert_underscores, **processed_params
    )


# ============================================================================
# ANALYSIS NOTES FOR APPROACH 2
# ============================================================================
"""
PROS:
1. Massive signature reduction
   - Functions become much shorter (5-15 lines instead of 300+)
   - Original: ~326 lines per function (Path example)
   - With hybrid: ~15-30 lines per function
   - For 7 functions: ~2,100 lines → ~150-200 lines (90% reduction)

2. Flexibility maintained for function-specific params
   - convert_underscores, embed, media_type remain explicit
   - Clear which parameters are unique to each function
   - Maintains self-documenting code for special cases

3. Simple implementation
   - No complex type aliasing
   - Straightforward forwarding pattern
   - Easy to understand and maintain

4. Type checking straightforward
   - MyPy should handle **kwargs forwarding well
   - Function-specific params have full type annotations

5. Reduced maintenance burden
   - Common parameter changes only affect helper/docs
   - Function-specific params still discoverable

CONS:
1. **CRITICAL**: Complete loss of IDE support for common params
   - IDEs cannot infer parameter names from **kwargs
   - No autocomplete for title, description, gt, ge, etc.
   - No tooltip hints when typing parameter names
   - **DEALBREAKER for developer experience**

2. **CRITICAL**: Loss of type checking for common params
   - MyPy cannot validate parameter names in **kwargs
   - Typos won't be caught (e.g., 'tittle' instead of 'title')
   - No type validation for parameter values
   - **DEALBREAKER for type safety**

3. Discovery problems
   - Developers must read documentation to know available parameters
   - Cannot rely on IDE suggestions
   - Harder to learn the API

4. Function signatures not self-documenting
   - Can't see at a glance what parameters are available
   - Must refer to COMMON_PARAM_DOCS or source code

5. Inconsistent with Python conventions
   - Python generally favors explicit over implicit
   - **kwargs is typically for truly open-ended parameters
   - FastAPI's current explicit approach is more Pythonic

6. Documentation generation concerns
   - May not properly generate OpenAPI schema
   - FastAPI introspection depends on explicit parameters
   - Could break automatic documentation features

ESTIMATED LOC REDUCTION: ~90% (from 2,100 to ~200 lines)

RISK ASSESSMENT: VERY HIGH
- Loss of IDE support is unacceptable for FastAPI's DX standards
- Loss of type checking defeats the purpose of Python type hints
- While achieving maximum LOC reduction, it sacrifices too much

RECOMMENDATION: DO NOT PURSUE
- The trade-offs are too severe
- IDE support and type safety are core requirements
- LOC reduction not worth the loss in developer experience
- Would represent a regression from current implementation

ALTERNATIVE VARIATION:
Could consider a partial hybrid where only 5-10 least-used parameters 
go into **kwargs, keeping commonly-used ones explicit. However, this 
still has similar (though reduced) IDE/type checking issues.
"""
