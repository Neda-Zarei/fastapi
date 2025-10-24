"""
Prototype Approach 1: Shared Type Constants

This approach extracts common parameter definitions to shared Annotated types.
The goal is to reduce duplication while maintaining IDE support for Doc() annotations.

Testing functions: Path, Query, Body (representing different param categories)
"""

from typing import Any, Callable, Dict, List, Optional, Union

from annotated_doc import Doc
from fastapi import params
from fastapi._compat import Undefined
from fastapi.openapi.models import Example
from typing_extensions import Annotated, deprecated

_Unset: Any = Undefined

# ============================================================================
# SHARED TYPE CONSTANTS - Common Parameters
# ============================================================================

# These type definitions include both the type and the Doc() annotation,
# allowing them to be reused across multiple functions while preserving
# IDE tooltip visibility.

_DefaultParam = Annotated[
    Any,
    Doc(
        """
        Default value if the parameter field is not set.
        """
    ),
]

_DefaultFactoryParam = Annotated[
    Union[Callable[[], Any], None],
    Doc(
        """
        A callable to generate the default value.

        This doesn't affect `Path` parameters as the value is always required.
        The parameter is available only for compatibility.
        """
    ),
]

_AliasParam = Annotated[
    Optional[str],
    Doc(
        """
        An alternative name for the parameter field.

        This will be used to extract the data and for the generated OpenAPI.
        It is particularly useful when you can't use the name you want because it
        is a Python reserved keyword or similar.
        """
    ),
]

_AliasPriorityParam = Annotated[
    Union[int, None],
    Doc(
        """
        Priority of the alias. This affects whether an alias generator is used.
        """
    ),
]

_ValidationAliasParam = Annotated[
    Union[str, None],
    Doc(
        """
        'Whitelist' validation step. The parameter field will be the single one
        allowed by the alias or set of aliases defined.
        """
    ),
]

_SerializationAliasParam = Annotated[
    Union[str, None],
    Doc(
        """
        'Blacklist' validation step. The vanilla parameter field will be the
        single one of the alias' or set of aliases' fields and all the other
        fields will be ignored at serialization time.
        """
    ),
]

_TitleParam = Annotated[
    Optional[str],
    Doc(
        """
        Human-readable title.
        """
    ),
]

_DescriptionParam = Annotated[
    Optional[str],
    Doc(
        """
        Human-readable description.
        """
    ),
]

_GtParam = Annotated[
    Optional[float],
    Doc(
        """
        Greater than. If set, value must be greater than this. Only applicable to
        numbers.
        """
    ),
]

_GeParam = Annotated[
    Optional[float],
    Doc(
        """
        Greater than or equal. If set, value must be greater than or equal to
        this. Only applicable to numbers.
        """
    ),
]

_LtParam = Annotated[
    Optional[float],
    Doc(
        """
        Less than. If set, value must be less than this. Only applicable to numbers.
        """
    ),
]

_LeParam = Annotated[
    Optional[float],
    Doc(
        """
        Less than or equal. If set, value must be less than or equal to this.
        Only applicable to numbers.
        """
    ),
]

_MinLengthParam = Annotated[
    Optional[int],
    Doc(
        """
        Minimum length for strings.
        """
    ),
]

_MaxLengthParam = Annotated[
    Optional[int],
    Doc(
        """
        Maximum length for strings.
        """
    ),
]

_PatternParam = Annotated[
    Optional[str],
    Doc(
        """
        RegEx pattern for strings.
        """
    ),
]

_RegexParam = Annotated[
    Optional[str],
    Doc(
        """
        RegEx pattern for strings.
        """
    ),
    deprecated(
        "Deprecated in FastAPI 0.100.0 and Pydantic v2, use `pattern` instead."
    ),
]

_DiscriminatorParam = Annotated[
    Union[str, None],
    Doc(
        """
        Parameter field name for discriminating the type in a tagged union.
        """
    ),
]

_StrictParam = Annotated[
    Union[bool, None],
    Doc(
        """
        If `True`, strict validation is applied to the field.
        """
    ),
]

_MultipleOfParam = Annotated[
    Union[float, None],
    Doc(
        """
        Value must be a multiple of this. Only applicable to numbers.
        """
    ),
]

_AllowInfNanParam = Annotated[
    Union[bool, None],
    Doc(
        """
        Allow `inf`, `-inf`, `nan`. Only applicable to numbers.
        """
    ),
]

_MaxDigitsParam = Annotated[
    Union[int, None],
    Doc(
        """
        Maximum number of allow digits for strings.
        """
    ),
]

_DecimalPlacesParam = Annotated[
    Union[int, None],
    Doc(
        """
        Maximum number of decimal places allowed for numbers.
        """
    ),
]

_ExamplesParam = Annotated[
    Optional[List[Any]],
    Doc(
        """
        Example values for this field.
        """
    ),
]

_ExampleParam = Annotated[
    Optional[Any],
    deprecated(
        "Deprecated in OpenAPI 3.1.0 that now uses JSON Schema 2020-12, "
        "although still supported. Use examples instead."
    ),
]

_OpenAPIExamplesParam = Annotated[
    Optional[Dict[str, Example]],
    Doc(
        """
        OpenAPI-specific examples.

        It will be added to the generated OpenAPI (e.g. visible at `/docs`).

        Swagger UI (that provides the `/docs` interface) has better support for the
        OpenAPI-specific examples than the JSON Schema `examples`, that's the main
        use case for this.

        Read more about it in the
        [FastAPI docs for Declare Request Example Data](https://fastapi.tiangolo.com/tutorial/schema-extra-example/#using-the-openapi_examples-parameter).
        """
    ),
]

_DeprecatedParam = Annotated[
    Union[deprecated, str, bool, None],
    Doc(
        """
        Mark this parameter field as deprecated.

        It will affect the generated OpenAPI (e.g. visible at `/docs`).
        """
    ),
]

_IncludeInSchemaParam = Annotated[
    bool,
    Doc(
        """
        To include (or not) this parameter field in the generated OpenAPI.
        You probably don't need it, but it's available.

        This affects the generated OpenAPI (e.g. visible at `/docs`).
        """
    ),
]

_JsonSchemaExtraParam = Annotated[
    Union[Dict[str, Any], None],
    Doc(
        """
        Any additional JSON schema data.
        """
    ),
]

_ExtraKwargs = Annotated[
    Any,
    Doc(
        """
        Include extra fields used by the JSON Schema.
        """
    ),
    deprecated(
        """
        The `extra` kwargs is deprecated. Use `json_schema_extra` instead.
        """
    ),
]

# ============================================================================
# FUNCTION IMPLEMENTATIONS - Using Shared Type Constants
# ============================================================================


def Path(  # noqa: N802
    default: _DefaultParam = ...,
    *,
    default_factory: _DefaultFactoryParam = _Unset,
    alias: _AliasParam = None,
    alias_priority: _AliasPriorityParam = _Unset,
    validation_alias: _ValidationAliasParam = None,
    serialization_alias: _SerializationAliasParam = None,
    title: _TitleParam = None,
    description: _DescriptionParam = None,
    gt: _GtParam = None,
    ge: _GeParam = None,
    lt: _LtParam = None,
    le: _LeParam = None,
    min_length: _MinLengthParam = None,
    max_length: _MaxLengthParam = None,
    pattern: _PatternParam = None,
    regex: _RegexParam = None,
    discriminator: _DiscriminatorParam = None,
    strict: _StrictParam = _Unset,
    multiple_of: _MultipleOfParam = _Unset,
    allow_inf_nan: _AllowInfNanParam = _Unset,
    max_digits: _MaxDigitsParam = _Unset,
    decimal_places: _DecimalPlacesParam = _Unset,
    examples: _ExamplesParam = None,
    example: _ExampleParam = _Unset,
    openapi_examples: _OpenAPIExamplesParam = None,
    deprecated: _DeprecatedParam = None,
    include_in_schema: _IncludeInSchemaParam = True,
    json_schema_extra: _JsonSchemaExtraParam = None,
    **extra: _ExtraKwargs,
) -> Any:
    """
    Declare a path parameter for a *path operation*.

    Read more about it in the
    [FastAPI docs for Path Parameters and Numeric Validations](https://fastapi.tiangolo.com/tutorial/path-params-numeric-validations/).

    ```python
    from typing import Annotated

    from fastapi import FastAPI, Path

    app = FastAPI()


    @app.get("/items/{item_id}")
    async def read_items(
        item_id: Annotated[int, Path(title="The ID of the item to get")],
    ):
        return {"item_id": item_id}
    ```
    """
    return params.Path(
        default=default,
        default_factory=default_factory,
        alias=alias,
        alias_priority=alias_priority,
        validation_alias=validation_alias,
        serialization_alias=serialization_alias,
        title=title,
        description=description,
        gt=gt,
        ge=ge,
        lt=lt,
        le=le,
        min_length=min_length,
        max_length=max_length,
        pattern=pattern,
        regex=regex,
        discriminator=discriminator,
        strict=strict,
        multiple_of=multiple_of,
        allow_inf_nan=allow_inf_nan,
        max_digits=max_digits,
        decimal_places=decimal_places,
        example=example,
        examples=examples,
        openapi_examples=openapi_examples,
        deprecated=deprecated,
        include_in_schema=include_in_schema,
        json_schema_extra=json_schema_extra,
        **extra,
    )


def Query(  # noqa: N802
    default: _DefaultParam = Undefined,
    *,
    default_factory: _DefaultFactoryParam = _Unset,
    alias: _AliasParam = None,
    alias_priority: _AliasPriorityParam = _Unset,
    validation_alias: _ValidationAliasParam = None,
    serialization_alias: _SerializationAliasParam = None,
    title: _TitleParam = None,
    description: _DescriptionParam = None,
    gt: _GtParam = None,
    ge: _GeParam = None,
    lt: _LtParam = None,
    le: _LeParam = None,
    min_length: _MinLengthParam = None,
    max_length: _MaxLengthParam = None,
    pattern: _PatternParam = None,
    regex: _RegexParam = None,
    discriminator: _DiscriminatorParam = None,
    strict: _StrictParam = _Unset,
    multiple_of: _MultipleOfParam = _Unset,
    allow_inf_nan: _AllowInfNanParam = _Unset,
    max_digits: _MaxDigitsParam = _Unset,
    decimal_places: _DecimalPlacesParam = _Unset,
    examples: _ExamplesParam = None,
    example: _ExampleParam = _Unset,
    openapi_examples: _OpenAPIExamplesParam = None,
    deprecated: _DeprecatedParam = None,
    include_in_schema: _IncludeInSchemaParam = True,
    json_schema_extra: _JsonSchemaExtraParam = None,
    **extra: _ExtraKwargs,
) -> Any:
    return params.Query(
        default=default,
        default_factory=default_factory,
        alias=alias,
        alias_priority=alias_priority,
        validation_alias=validation_alias,
        serialization_alias=serialization_alias,
        title=title,
        description=description,
        gt=gt,
        ge=ge,
        lt=lt,
        le=le,
        min_length=min_length,
        max_length=max_length,
        pattern=pattern,
        regex=regex,
        discriminator=discriminator,
        strict=strict,
        multiple_of=multiple_of,
        allow_inf_nan=allow_inf_nan,
        max_digits=max_digits,
        decimal_places=decimal_places,
        example=example,
        examples=examples,
        openapi_examples=openapi_examples,
        deprecated=deprecated,
        include_in_schema=include_in_schema,
        json_schema_extra=json_schema_extra,
        **extra,
    )


def Body(  # noqa: N802
    default: _DefaultParam = Undefined,
    *,
    default_factory: _DefaultFactoryParam = _Unset,
    embed: Annotated[
        Union[bool, None],
        Doc(
            """
            Whether to embed the body parameter in the request.

            If `True`, the parameter will be expected as a key in the JSON body,
            instead of being the whole body itself.
            """
        ),
    ] = None,
    media_type: Annotated[
        str,
        Doc(
            """
            The media type for this body parameter.
            """
        ),
    ] = "application/json",
    alias: _AliasParam = None,
    alias_priority: _AliasPriorityParam = _Unset,
    validation_alias: _ValidationAliasParam = None,
    serialization_alias: _SerializationAliasParam = None,
    title: _TitleParam = None,
    description: _DescriptionParam = None,
    gt: _GtParam = None,
    ge: _GeParam = None,
    lt: _LtParam = None,
    le: _LeParam = None,
    min_length: _MinLengthParam = None,
    max_length: _MaxLengthParam = None,
    pattern: _PatternParam = None,
    regex: _RegexParam = None,
    discriminator: _DiscriminatorParam = None,
    strict: _StrictParam = _Unset,
    multiple_of: _MultipleOfParam = _Unset,
    allow_inf_nan: _AllowInfNanParam = _Unset,
    max_digits: _MaxDigitsParam = _Unset,
    decimal_places: _DecimalPlacesParam = _Unset,
    examples: _ExamplesParam = None,
    example: _ExampleParam = _Unset,
    openapi_examples: _OpenAPIExamplesParam = None,
    deprecated: _DeprecatedParam = None,
    include_in_schema: _IncludeInSchemaParam = True,
    json_schema_extra: _JsonSchemaExtraParam = None,
    **extra: _ExtraKwargs,
) -> Any:
    return params.Body(
        default=default,
        default_factory=default_factory,
        embed=embed,
        media_type=media_type,
        alias=alias,
        alias_priority=alias_priority,
        validation_alias=validation_alias,
        serialization_alias=serialization_alias,
        title=title,
        description=description,
        gt=gt,
        ge=ge,
        lt=lt,
        le=le,
        min_length=min_length,
        max_length=max_length,
        pattern=pattern,
        regex=regex,
        discriminator=discriminator,
        strict=strict,
        multiple_of=multiple_of,
        allow_inf_nan=allow_inf_nan,
        max_digits=max_digits,
        decimal_places=decimal_places,
        example=example,
        examples=examples,
        openapi_examples=openapi_examples,
        deprecated=deprecated,
        include_in_schema=include_in_schema,
        json_schema_extra=json_schema_extra,
        **extra,
    )


# ============================================================================
# ANALYSIS NOTES FOR APPROACH 1
# ============================================================================
"""
PROS:
1. Significant LOC reduction: ~60-70% reduction in documentation lines
   - Original: ~326 lines per function (Path example)
   - With shared types: ~60-80 lines per function + ~400 lines of shared defs
   - For 7 functions: ~2,100 lines → ~960 lines (54% reduction)

2. Single source of truth for parameter documentation
   - Updating a parameter's Doc() only needs one change
   - Consistency guaranteed across all functions

3. Type annotations remain clear
   - Each parameter still has explicit type information
   - IDE can infer types from the shared constants

4. Maintainability improvement
   - New common parameters added in one place
   - Reduced risk of inconsistencies between functions

CONS:
1. IDE tooltip visibility - CRITICAL CONCERN
   - Depends on IDE's ability to resolve Annotated type aliases
   - VSCode/Pylance: May show "_TitleParam" instead of Doc() content
   - PyCharm: May or may not resolve the aliased type correctly
   - **NEEDS TESTING WITH ACTUAL IDE**

2. Reduced readability for newcomers
   - Function signatures reference _ParamName constants
   - Developers must jump to definition to see Doc() content
   - Less self-documenting code

3. Indirection adds cognitive load
   - Understanding what a parameter does requires navigation
   - Not as explicit as having Doc() inline

4. Type alias resolution complexity
   - MyPy needs to correctly resolve nested Annotated types
   - Potential issues with strict mode checking
   - **NEEDS TESTING WITH MYPY STRICT**

5. Function-specific parameters still inline
   - embed, media_type, convert_underscores cannot use shared types
   - Creates inconsistency in parameter definition style

ESTIMATED LOC REDUCTION: ~54% (from 2,100 to 960 lines)

RISK ASSESSMENT: MEDIUM-HIGH
- Main risk: IDE tooltip degradation
- If IDEs don't show Doc() content on hover, this approach fails requirement
- Type checking should work but needs validation

RECOMMENDATION FOR TESTING:
1. Test in VSCode with Pylance
2. Test in PyCharm
3. Run mypy --strict
4. Compare tooltip behavior with original implementation
"""
