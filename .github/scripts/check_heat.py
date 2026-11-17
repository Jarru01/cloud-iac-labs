"""Offline sanity check for OpenStack Heat templates.

Heat has no offline validator, so this catches the mistakes that are easy to
make by hand: YAML errors, missing top-level keys, and get_param /
get_resource / get_attr / depends_on / condition references that point at
parameters, resources or conditions that do not exist.

Usage: python check_heat.py openstack1/*.yml openstack2/*.yml
"""

import sys

import yaml

PSEUDO_PARAMS = {"OS::stack_name", "OS::stack_id", "OS::project_id"}


def walk(node):
    """Yield (function, argument) for every intrinsic function call."""
    if isinstance(node, dict):
        for key, value in node.items():
            if key in ("get_param", "get_resource", "get_attr"):
                yield key, value
            yield from walk(value)
    elif isinstance(node, list):
        for item in node:
            yield from walk(item)


def check(path):
    errors = []
    with open(path, encoding="utf-8") as fh:
        try:
            tpl = yaml.safe_load(fh)
        except yaml.YAMLError as exc:
            return [f"invalid YAML: {exc}"]

    for key in ("heat_template_version", "resources"):
        if key not in tpl:
            errors.append(f"missing top-level key '{key}'")

    params = set(tpl.get("parameters") or {}) | PSEUDO_PARAMS
    resources = tpl.get("resources") or {}
    conditions = set(tpl.get("conditions") or {})

    for fn, arg in walk({"resources": resources, "outputs": tpl.get("outputs") or {}}):
        name = arg[0] if isinstance(arg, list) else arg
        if not isinstance(name, str):
            continue
        if fn == "get_param" and name not in params:
            errors.append(f"get_param: unknown parameter '{name}'")
        if fn in ("get_resource", "get_attr") and name not in resources:
            errors.append(f"{fn}: unknown resource '{name}'")

    for res_name, res in resources.items():
        deps = res.get("depends_on") or []
        for dep in [deps] if isinstance(deps, str) else deps:
            if dep not in resources:
                errors.append(f"{res_name}: depends_on unknown resource '{dep}'")
        cond = res.get("condition")
        if isinstance(cond, str) and cond not in conditions:
            errors.append(f"{res_name}: unknown condition '{cond}'")
        if "type" not in res:
            errors.append(f"{res_name}: missing 'type'")
    return errors


def main(paths):
    failed = False
    for path in paths:
        errors = check(path)
        status = "FAIL" if errors else "ok"
        print(f"{status:4} {path}")
        for err in errors:
            print(f"     - {err}")
        failed |= bool(errors)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
