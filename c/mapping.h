#ifndef _MAPPING_
#define _MAPPING_

int open_physical (int fd);
void close_physical (int fd);
void* map_physical(int fd, unsigned int base, unsigned int span);
int unmap_physical(void * virtual_base, unsigned int span);


#endif