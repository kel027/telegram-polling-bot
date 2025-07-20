# Changelog

All notable changes to the Telegram Polling Bot Framework are documented here, following [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-05-22

### Added
- Unified async architecture (`polling_bot_unified.py`)
- Performance profiling with py-spy
- Graceful shutdown with resource cleanup
- Comprehensive error handling
- Detailed performance metrics

### Changed
- Migrated to unified async architecture
- Improved first vote processing by 91% (130ms → 12ms)
- Enhanced resource management
- Improved scalability

### Performance
- **91% faster first vote processing** (130ms → 12ms); subsequent votes equal (12ms)
- **70% reduction** in thread worker overhead
- **56% less GIL contention** (16% → 7%)
- **55% fewer threads** at completion (11 → 5)
- **Startup latency** reduced (0.957s → 0.732s)
- **Poll creation latency** reduced (0.903s → 0.865s)
- **Image send latency** reduced (0.436s → 0.417s)
- Single event loop eliminates thread coordination
- Reduced memory footprint by 50%

## [1.0.0] - 2024-04-01

### Added
- Threading-based coroutines (`polling_bot_threading.py`)
- Core polling with automated lifecycle
- Image support for poll attachment
- MongoDB integration for vote/poll storage
- Basic error handling and logging
- Multi-threaded architecture

### Features
- Poll creation/management
- Reminder system
- Message cleanup
- Vote tracking

## Template for Future Releases

## [X.Y.Z] - YYYY-MM-DD

### Added
- New features

### Changed
- Changes in functionality

### Deprecated
- Features to be removed

### Removed
- Removed features

### Fixed
- Bug fixes

### Security
- Security improvements