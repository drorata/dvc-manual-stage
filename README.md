# Manual step as part of a `dvc` pipeline

## Objective

You want to include a stage in your pipeline which involves a manual process, and you want DVC to properly track the flow.
Here's a usecase.
You want to map words in a given text file using some manually crafted mapping of the existing words.
To achieve this you can follow these steps:

1. Extract the unique values of the input
2. Manually build the map (using the unique values)
3. Map the input using the manually crafted dictionary.

The solution should provide the following:

* If the raw data changes, the resulting mapped line should be invalidated
* If the mapping is changed (even without having the raw data changed) the mapped line should be invalidated

## Initial Solution

### Unique values

This is a simple and straightforward step; given an input you generate a JSON with the unique words in your input.

```bash
dvc add raw_data.txt
dvc run -d unique_values.py -d raw_data.txt -o unique_values.json python unique_values.py
```

### Crafting the map

Copy the output [`unique_values.json`](./unique_values.json) to [`mapping.json`](mapping.json).
Edit the JSON as per need.

### Mapping stage

The mapping stage depends on the following:

* The mapping code: [`mapping.py`](mapping.py)
* The mapping dictionary: [`mapping.json`](mapping.json)
* Lastly and implicitly, it also depends on the unique values extracted in the first stage.

So, the following looks reasonable:

```bash
dvc run -d mapping.py -d mapping.json -d unique_values.json -o mapped_line.txt python mapping.py
```

### Gotcha

Think what happens if the unique values changed (due to some change in the raw input).
The stage `mapped_line.txt.dvc` would be invalidated because the dependency `unique_values.json` has changed and will be re-run upon reproducing.
But, `dvc` will not stop you and know that `mapping.json` has changed; well, because it didn't.
The problem is that a change in the unique values should also invalidate the mapping.

## Better solution

Introduce a flag and empty file `MAPPING_IS_VALID`.
If this file exists, this would be an indication that the manual process involved in crafting `mapping.json` was completed.
The trick is threefold:

* `MAPPING_IS_VALID` will be deleted by the unique values stage and
* `MAPPING_IS_VALID` will be a dependency of the mapping stage
* `MAPPING_IS_VALID` is tracked neither by `git` nor by `dvc`

So, here are the stages:

```bash
# Determine the unique values
dvc run -d unique_values.py -d raw_data.txt -o unique_values.json "python unique_values.py && rm -f MAPPING_IS_VALID"
```

and

```bash
# Map the value
dvc run -d mapping.py -d mapping.json -d unique_values.json -d MAPPING_IS_VALID -o mapped_line.txt python mapping.py
```
