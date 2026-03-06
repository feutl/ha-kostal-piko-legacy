# Release Workflow

This document outlines the correct process for creating releases of the Kostal Piko Legacy integration.

## Release Checklist

Follow these steps **in order** to create a new release:

### 1. Update Version Numbers
Update the version in these files:
- `custom_components/kostal/manifest.json` - Update `version` field
- `custom_components/kostal/__init__.py` - Update `__version__` variable

### 2. Update CHANGELOG.md
Add a new section at the top with:
- Version number and date
- Changed/Added/Fixed/Removed items
- Any testing notes or important information

### 3. Commit and Push Changes
```bash
# Stage the changes
git add CHANGELOG.md custom_components/kostal/manifest.json custom_components/kostal/__init__.py

# Commit with descriptive message
git commit -m "Release vX.X.X - Brief description

- Change 1
- Change 2
- Change 3"

# Push to GitHub
git push origin master
```

### 4. Create Git Tag
```bash
# Create the tag
git tag vX.X.X

# Push the tag to GitHub
git push origin vX.X.X
```

### 5. Create GitHub Release
```bash
# For pre-releases (rc, beta, alpha)
gh release create vX.X.X-rc.Y \
  --title "vX.X.X-rc.Y - Title" \
  --notes "Release notes here" \
  --prerelease

# For stable releases
gh release create vX.X.X \
  --title "vX.X.X - Title" \
  --notes "Release notes here"
```

## ⚠️ Common Mistakes to Avoid

1. **DO NOT** create the GitHub release before committing and pushing changes
2. **DO NOT** create the tag before committing changes
3. **Always** follow the order: commit → push → tag → push tag → GitHub release

## Version Numbering

This project follows [Semantic Versioning](https://semver.org/):
- **MAJOR.MINOR.PATCH** (e.g., 1.3.1)
- **MAJOR.MINOR.PATCH-rc.X** for release candidates
- **MAJOR.MINOR.PATCH-beta.X** for beta releases

Examples:
- `1.3.1` - Stable release
- `1.3.1-rc.1` - First release candidate for 1.3.1
- `1.4.0-beta.1` - First beta for 1.4.0

## Release Types

### Release Candidate (rc)
Pre-release for testing before stable release. Use `--prerelease` flag.

```bash
gh release create v1.3.1-rc.1 --title "v1.3.1-rc.1 - Description" --notes "..." --prerelease
```

### Stable Release
Final production-ready release.

```bash
gh release create v1.3.1 --title "v1.3.1 - Description" --notes "..."
```

## Quick Reference

**Correct Order:**
1. Update version files
2. Update CHANGELOG.md
3. `git add` → `git commit` → `git push`
4. `git tag vX.X.X` → `git push origin vX.X.X`
5. `gh release create`

**If you mess up:**
```bash
# Delete local tag
git tag -d vX.X.X

# Delete remote tag
git push origin :refs/tags/vX.X.X

# Recreate tag on correct commit
git tag vX.X.X

# Force push the corrected tag
git push origin vX.X.X --force
```
