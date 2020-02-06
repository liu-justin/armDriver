#include <stdio.h>
#include <stdlib.h>

#include "MotorVector.h"

MotorVector::MotorVector() {
    _capacity = VECTOR_INIT_CAPACITY;
    _total = 0;
    _items = malloc(sizeof(void *) * _capacity);
}

int MotorVector::total()
{
    return _total;
}

static void MotorVector::resize(int incomingCapacity)
{
    #ifdef DEBUG_ON
    printf("vector_resize: %d to %d\n", _capacity, incomingCapacity);
    #endif

    void **items = realloc(_items, sizeof(void *) * _capacity);
    if (items) {
        _items = items;
        _capacity = incomingCapacity;
    }
}

void MotorVector::add(void *item)
{
    if (_capacity == _total)
        resize(_capacity * 2);
    v->items[v->total++] = item;
}

void MotorVector::get(int index)
{
    if (index >= 0 && index < _total)
        return _items[index];
    return NULL;
}

void MotorVector::free()
{
    free(_items);
}