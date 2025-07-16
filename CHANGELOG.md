# Changelog

All notable changes to the Telegram Polling Bot Framework will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-05-22

### Added
- **Unified async architecture** implementation (`polling_bot_unified.py`)
- Telegram Polling Bot Framework with automated poll lifecycle
- MongoDB integration for vote and poll storage
- Image support for poll attachments
- Environment variable configuration
- Production deployment guide with cron job examples
- Performance profiling with py-spy integration
- Graceful shutdown with proper resource cleanup
- Comprehensive error handling and validation
- Performance analysis with detailed metrics comparison

### Changed
- Migrated from threading-based to unified async architecture
- Improved vote processing performance by 91%
- Enhanced resource management and memory usage
- Better scalability characteristics

### Performance
- **91% faster vote processing** (164ms → 15ms)
- **70% reduction** in thread worker overhead
- **56% less GIL contention** (16% → 7%)
- **55% fewer threads** at completion (11 → 5)
- Single event loop design eliminating thread coordination overhead
- Cooperative task scheduling for better responsiveness
- Reduced memory footprint by 50%
- Eliminated context switching penalties

## [1.0.0] - 2024-04-01

### Added
- **Threading-based coroutines** implementation (`polling_bot_threading.py`)
- Core polling functionality with automated lifecycle
- MongoDB vote collection and storage
- Basic error handling and logging
- Multi-threaded architecture with separate event loops

### Features
- Poll creation and management
- Reminder system before poll closure
- Message cleanup and deletion
- Database operations for vote tracking

---

## Template for Future Releases

## [X.Y.Z] - YYYY-MM-DD

### Added
- New features

### Changed
- Changes in existing functionality

### Deprecated
- Soon-to-be removed features

### Removed
- Removed features

### Fixed
- Bug fixes

### Security
- Security improvements
