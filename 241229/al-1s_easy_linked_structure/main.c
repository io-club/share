#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <stdlib.h>

typedef struct Shop
{
    int j;
    int f;
    float mp;
} Shop;

typedef struct Link
{
    struct Link *prev;
    struct Link *next;
    const Shop *shop;
} Link;

void print_link(Link *link)
{
    if (link->shop)
        printf("Shop(%d, %d)", link->shop->j, link->shop->f);
    else
        printf("Shop(NULL)");
}

int main()
{
    const char *FORMAT = "%d%d";
    int m, n;
    scanf(FORMAT, &m, &n);
    Link begin = {NULL, NULL, NULL};
    Link end = {&begin, NULL, NULL};
    begin.next = &end;
    for (int i = 0; i < n; i++)
    {
        // printf("Begin from: ");
        // print_link(begin.next);
        // printf("\n");
        // printf("Curr list: [");
        // int x = 0;
        for (Link *curr = begin.next; curr && curr->shop; curr = curr->next)
        {
            const Shop *const shop = curr->shop;
            const int j = shop->j;
            const int f = shop->f;
            // printf("%d %d, ", j, f);
            // if (++x == 10)
            //     break;
        }
        // printf("]\n");

        int j, f;
        scanf(FORMAT, &j, &f);
        const float mp = (float)j / f;
        for (Link *curr = begin.next; curr; curr = curr->next)
        {
            if (!curr->shop || mp >= curr->shop->mp)
            {
                // printf("S: %d %d %f\n", j, f, mp);
                Link *prev = curr->prev;
                // printf("PREV: ");
                // print_link(prev);
                // printf("\n");

                // printf("CURR: ");
                // print_link(curr);
                // printf("\n");
                // if (prev->shop) printf("PREV S: %d %d\n", prev->shop->j, prev->shop->f);
                // if (curr->shop) printf("CURR S: %d %d\n", curr->shop->j, curr->shop->f);
                // printf("BEGIN FROM: ");
                // print_link(begin.next);
                // printf("\n");
                Shop *const shop = malloc(sizeof(Shop));
                *shop = (Shop){j, f, mp};
                // const Shop shop = { j, f, mp };
                Link *link = malloc(sizeof(Link));
                *link = (Link){prev, curr, shop};
                prev->next = link;
                // printf("pn and bn: %d\n", prev->next == begin.next);
                curr->prev = link;
                // printf("Now begin from: ");
                // print_link(begin.next);
                // printf("\nAnd for the prev:");
                // printf("%d", prev == &begin);
                // print_link(prev->next);
                // printf("\n");
                break;
            }
        }
        // printf("MP: %f\n", mp);
    }
    // printf("END\n");
    float pt = 0, money = (float)m;
    for (Link *curr = begin.next; curr && curr->shop; curr = curr->next)
    {
        // printf("PT: %f\n", pt);
        const Shop *const shop = curr->shop;
        const int j = shop->j;
        const int f = shop->f;
        // printf("S: %d %d %d\n", j, f, curr->next == NULL);
        if (money < f)
        {
            pt += money / f * j;
            break;
        }
        pt += j;
        money -= f;
    }
    printf("%.3f", pt);
    return 0;
}
