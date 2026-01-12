"""API rate limiter using token bucket algorithm"""

import time
from typing import Dict
import asyncio


class TokenBucket:
    """
    Token bucket rate limiter

    Allows burst of requests up to capacity, then refills at a steady rate.
    """

    def __init__(self, capacity: int, refill_rate: float):
        """
        Initialize token bucket

        Args:
            capacity: Maximum number of tokens (requests)
            refill_rate: Tokens added per second
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.time()
        self._lock = asyncio.Lock()

    async def consume(self, tokens: int = 1) -> bool:
        """
        Try to consume tokens

        Args:
            tokens: Number of tokens to consume

        Returns:
            bool: True if tokens were consumed, False if not enough tokens
        """
        async with self._lock:
            # Refill tokens based on time elapsed
            now = time.time()
            elapsed = now - self.last_refill
            self.tokens = min(
                self.capacity,
                self.tokens + (elapsed * self.refill_rate)
            )
            self.last_refill = now

            # Check if we have enough tokens
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True

            return False

    async def wait_for_tokens(self, tokens: int = 1):
        """
        Wait until tokens are available

        Args:
            tokens: Number of tokens needed
        """
        while not await self.consume(tokens):
            # Calculate wait time
            tokens_needed = tokens - self.tokens
            wait_time = tokens_needed / self.refill_rate
            await asyncio.sleep(min(wait_time, 1.0))  # Max 1 second waits

    def get_available_tokens(self) -> float:
        """Get current number of available tokens"""
        now = time.time()
        elapsed = now - self.last_refill
        return min(
            self.capacity,
            self.tokens + (elapsed * self.refill_rate)
        )

    def get_wait_time(self, tokens: int = 1) -> float:
        """
        Get estimated wait time for tokens

        Args:
            tokens: Number of tokens needed

        Returns:
            float: Wait time in seconds (0 if tokens available)
        """
        available = self.get_available_tokens()
        if available >= tokens:
            return 0.0

        tokens_needed = tokens - available
        return tokens_needed / self.refill_rate


class RateLimiter:
    """
    Global rate limiter for API requests

    Manages multiple endpoints with different limits
    """

    def __init__(self):
        self.buckets: Dict[str, TokenBucket] = {}
        self._setup_default_limits()

    def _setup_default_limits(self):
        """Setup default rate limits for Alpaca API"""
        # Alpaca limits: 200 requests/minute
        self.buckets['alpaca'] = TokenBucket(
            capacity=200,
            refill_rate=200 / 60  # ~3.33 tokens per second
        )

        # Data endpoints (more restrictive)
        self.buckets['alpaca_data'] = TokenBucket(
            capacity=100,
            refill_rate=100 / 60  # ~1.67 tokens per second
        )

        # Trading endpoints
        self.buckets['alpaca_trading'] = TokenBucket(
            capacity=200,
            refill_rate=200 / 60
        )

    async def check_limit(self, endpoint: str = 'alpaca') -> bool:
        """
        Check if request is allowed

        Args:
            endpoint: Endpoint identifier

        Returns:
            bool: True if request allowed
        """
        bucket = self.buckets.get(endpoint)
        if not bucket:
            return True  # No limit for unknown endpoints

        return await bucket.consume(1)

    async def wait_for_limit(self, endpoint: str = 'alpaca'):
        """
        Wait until request is allowed

        Args:
            endpoint: Endpoint identifier
        """
        bucket = self.buckets.get(endpoint)
        if not bucket:
            return

        await bucket.wait_for_tokens(1)

    def get_status(self) -> Dict:
        """
        Get rate limit status for all endpoints

        Returns:
            Dict with status for each endpoint
        """
        status = {}

        for name, bucket in self.buckets.items():
            available = bucket.get_available_tokens()
            status[name] = {
                'capacity': bucket.capacity,
                'available': int(available),
                'refill_rate': bucket.refill_rate,
                'percentage': (available / bucket.capacity) * 100,
            }

        return status

    def add_custom_limit(
        self,
        name: str,
        capacity: int,
        refill_rate: float
    ):
        """
        Add custom rate limit

        Args:
            name: Limit identifier
            capacity: Maximum tokens
            refill_rate: Tokens per second
        """
        self.buckets[name] = TokenBucket(capacity, refill_rate)


# Global rate limiter instance
rate_limiter = RateLimiter()
