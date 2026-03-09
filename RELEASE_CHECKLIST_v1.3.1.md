# Release Checklist for v1.3.1

## ✅ COMPLETED - Documentation & Code Updates

All documentation has been updated and the code is ready for stable release v1.3.1.

### Files Updated

1. ✅ **CHANGELOG.md**
   - Added comprehensive v1.3.1 stable release entry (dated 2026-03-09)
   - Consolidated all changes from release candidates
   - Documented fixes, changes, improvements, and testing

2. ✅ **README.md**
   - Updated version to 1.3.1
   - Added "What's New in 1.3.1" section
   - Added reference to CHANGELOG.md
   - All content verified and accurate

3. ✅ **IMPROVEMENTS.md**
   - Reorganized to show completed work
   - Marked all v1.3.1 tasks as complete ✅
   - Maintained future roadmap
   - Added version history and testing checklist

4. ✅ **RELEASE.md**
   - Enhanced with concrete v1.3.1 release example
   - Added post-release checklist
   - Included helpful git commands

5. ✅ **.github/copilot-instructions.md** (NEW)
   - Comprehensive guide for AI assistants and developers
   - Complete coding standards and best practices
   - Implementation details and patterns
   - Testing guidelines and common tasks

6. ✅ **DOCUMENTATION_SUMMARY.md** (NEW)
   - Complete overview of all documentation
   - Status of each file
   - Next steps for release
   - Verification checklist

7. ✅ **custom_components/kostal/manifest.json**
   - Version updated: 1.3.1-rc.6 → 1.3.1

8. ✅ **custom_components/kostal/__init__.py**
   - Version updated: 1.3.1-rc.6 → 1.3.1

---

## 📋 NEXT STEPS - Release Process

Follow these commands **in order** to complete the release:

### Step 1: Review Changes
```bash
# Review what's changed
git status
git diff
```

### Step 2: Stage All Changes
```bash
git add .github/copilot-instructions.md
git add CHANGELOG.md
git add README.md
git add IMPROVEMENTS.md
git add RELEASE.md
git add DOCUMENTATION_SUMMARY.md
git add custom_components/kostal/manifest.json
git add custom_components/kostal/__init__.py
```

### Step 3: Commit
```bash
git commit -m "Release v1.3.1 - Modernization and deprecation fixes

- Removed all deprecated code (CONNECTION_CLASS, @Throttle, hass.loop, hass.add_job)
- Updated to Home Assistant 2026 best practices
- Added options flow support for updating sensors
- Improved async patterns and code maintainability
- Updated all documentation
- Added comprehensive copilot instructions"
```

### Step 4: Push to GitHub
```bash
git push origin master
```

### Step 5: Create and Push Tag
```bash
git tag v1.3.1
git push origin v1.3.1
```

### Step 6: Create GitHub Release
```bash
gh release create v1.3.1 \
  --title "v1.3.1 - Modernization Release" \
  --notes "## What's New

✅ Fully compatible with Home Assistant 2026.3.0
✅ All deprecated code removed
✅ Options flow - update sensors after setup
✅ Modern async patterns
✅ Better code maintainability

## Changes
- Removed deprecated @Throttle, hass.loop, hass.add_job, and CONNECTION_CLASS
- Implemented options flow for updating monitored sensors
- Updated to current HA development best practices
- Added comprehensive documentation and copilot instructions

## Testing
Verified with Home Assistant 2026.3.0 - all features working correctly.

See [CHANGELOG.md](https://github.com/feutl/ha-kostal-piko-legacy/blob/master/CHANGELOG.md) for complete details."
```

---

## 🎯 What This Release Includes

### Code Improvements
- ✅ All deprecated code removed (HA 2026 compliant)
- ✅ Options flow for updating sensors post-setup
- ✅ Modern async/await patterns
- ✅ Clean, maintainable codebase

### Documentation
- ✅ Complete CHANGELOG with all changes
- ✅ Updated README with what's new
- ✅ Reorganized IMPROVEMENTS showing progress
- ✅ Enhanced RELEASE guide with examples
- ✅ New copilot instructions for AI assistance

### Quality
- ✅ No errors or warnings
- ✅ Tested with HA 2026.3.0
- ✅ All sensors working correctly
- ✅ Config flow and options flow verified

---

## 📊 Documentation Health Check

| Document | Status | Version | Last Updated |
|----------|--------|---------|--------------|
| CHANGELOG.md | ✅ Complete | 1.3.1 | 2026-03-09 |
| README.md | ✅ Complete | 1.3.1 | 2026-03-09 |
| IMPROVEMENTS.md | ✅ Complete | 1.3.1 | 2026-03-09 |
| RELEASE.md | ✅ Complete | Current | 2026-03-09 |
| copilot-instructions.md | ✅ New | 1.3.1 | 2026-03-09 |
| manifest.json | ✅ Complete | 1.3.1 | 2026-03-09 |
| __init__.py | ✅ Complete | 1.3.1 | 2026-03-09 |

---

## ✅ Pre-Release Verification

Before running the release commands, verify:

- ✅ All documentation updated and accurate
- ✅ Version numbers consistent (1.3.1)
- ✅ CHANGELOG has today's date (2026-03-09)
- ✅ No Python errors in code
- ✅ README reflects new features
- ✅ Copilot instructions created

---

## 🚀 You're Ready!

Everything is prepared for the v1.3.1 stable release. Simply follow the commands in the "NEXT STEPS" section above to complete the release process.

**Time to release:** ~3-5 minutes
**Risk level:** Low (all changes verified)

Good luck with the release! 🎉
